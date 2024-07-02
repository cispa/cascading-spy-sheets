import asyncio
from json import dumps

from loguru import logger
from playwright._impl._errors import Error, TimeoutError
from playwright.async_api import Browser, Request, Response, async_playwright

TRANCO_FILE = "tranco_LJ494.csv"
PAGE_TIMEOUT = 20000
DOMAIN_AMOUNT = 50


class QueryError:
    def __init__(self):
        self.code = None
        self.error = None

    def request_error(self, code: int) -> None:
        self.code = code

    def exception(self, error: str) -> None:
        self.error = error


class QueryResult:
    def __init__(self):
        self.requests = {"accumulatedRequestBodySize": 0, "requestCount": 0}
        self.responses = {"accumulatedResposeBodySize": 0, "responseCount": 0}
        self.error = None
        self.fcp = None
        self.navigationDuration = None
        self.resourceDuration = None

    def add_request(self, request: Request) -> None:
        self.requests["requestCount"] += 1
        if "content-length" in request.headers:
            self.requests["accumulatedRequestBodySize"] += int(
                request.headers["content-length"]
            )

    def add_response(self, response: Response) -> None:
        self.responses["responseCount"] += 1
        if "content-length" in response.headers:
            self.responses["accumulatedResposeBodySize"] += int(
                response.headers["content-length"]
            )

    def got_error(self, code: int | None = None, error: str | None = None) -> None:
        if not self.error:
            self.error = QueryError()
        if code:
            self.error.request_error(code)
        if error:
            self.error.exception(error)


async def query_domain(browser: Browser, domain: str) -> QueryResult:
    logger.debug(f"Querying {domain}")
    result = QueryResult()
    page = await browser.new_page()
    try:
        page.on("request", result.add_request)
        page.on("response", result.add_response)
        response = await page.goto(url=domain, wait_until="load", timeout=PAGE_TIMEOUT)
        if not response.ok:
            result.got_error(code=response.status)

        navigationPerformance = await page.evaluate(
            "performance.getEntriesByType('navigation')"
        )
        if navigationPerformance and "duration" in navigationPerformance[0]:
            result.navigationDuration = navigationPerformance[0]["duration"]

        resourcePerformance = await page.evaluate(
            "window.performance.getEntriesByType('resource')"
        )
        if resourcePerformance and "duration" in resourcePerformance[0]:
            result.resourceDuration = resourcePerformance[0]["duration"]

        firstContentfulPaint = await page.evaluate(
            "window.performance.getEntriesByType('paint')"
        )
        if firstContentfulPaint and "startTime" in firstContentfulPaint[0]:
            result.fcp = firstContentfulPaint[0]["startTime"]
    except TimeoutError:
        result.got_error(error="TimeoutError")
        logger.error(f"Page load timed out for {domain}")
    except Error as e:
        result.got_error(error=str(e))
        logger.error(f"Failed to query {domain}: {str(e)}")

    finally:
        if result.error and result.error.code:
            logger.error(
                f"Received error code {result.error.code} when requesting {domain}"
            )
        await page.close()
    return result


async def install_extension(firefox):
    context = firefox
    page = await context.new_page()
    await page.goto(
        "about:debugging#/runtime/this-firefox", wait_until="domcontentloaded"
    )
    await page.wait_for_timeout(20000)
    await page.close()


async def run_browser(
    domains: list[str], install_ext: bool = False
) -> dict[str, QueryResult]:
    async with async_playwright() as playwright:
        firefox = await playwright.firefox.launch(headless=not install_ext)
        if install_ext:
            await install_extension(firefox)

        results, successfull_queries = dict(), 0
        for domain in domains:
            if successfull_queries >= DOMAIN_AMOUNT:
                break
            result = await query_domain(firefox, domain)
            results[domain] = result
            if not result.error:
                successfull_queries += 1
    return results


def parse_domains(filename: str = TRANCO_FILE) -> list[str]:
    with open(filename) as fp:
        domains = ["https://" + line.strip().split(",")[-1] for line in fp.readlines()]
    return domains


def evaluate_requests(
    results: dict[str, QueryResult]
) -> dict[str, dict[str, int | float]]:
    evaluated_requests = dict()
    for domain, query_result in results.items():
        if query_result.error and query_result.error.error != "TimeoutError":
            logger.error(f"Error for {domain}: {query_result.error.error}")
            continue

        domain_result = {
            "requestCount": query_result.requests["requestCount"],
            "responseCount": query_result.responses["responseCount"],
        }

        if "accumulatedRequestBodySize" in query_result.requests:
            domain_result["accumulatedRequestBodySize"] = query_result.requests[
                "accumulatedRequestBodySize"
            ]

        if "accumulatedResposeBodySize" in query_result.responses:
            domain_result["accumulatedResposeBodySize"] = query_result.responses[
                "accumulatedResposeBodySize"
            ]

        if query_result.navigationDuration:
            domain_result["navigationDuration"] = query_result.navigationDuration

        if query_result.resourceDuration:
            domain_result["resourceDuration"] = query_result.resourceDuration

        if query_result.fcp:
            domain_result["fcp"] = query_result.fcp

        evaluated_requests[domain] = domain_result
    return evaluated_requests


def correlate_results(
    results1: dict[str, dict[str, int | float]],
    results2: dict[str, dict[str, int | float]],
) -> dict[str, dict[str, int | float]]:
    common_domains = set(results1.keys()).intersection(set(results2.keys()))
    correlated_results = {}
    for domain in common_domains:
        correlated_results[domain] = {
            key: results1[domain][key] - results2[domain][key]
            for key in set(results1[domain].keys()).intersection(
                set(results2[domain].keys())
            )
        }
    return correlated_results


def write_results(results: dict[str, dict[str, int | float]], filename: str) -> None:
    with open(filename, "w") as fp:
        fp.write(dumps(results, indent=4))


async def main():
    domains = parse_domains()

    logger.info(f"Starting Crawl with extension")
    results1 = await run_browser(domains, install_ext=True)
    evaluated_results1 = evaluate_requests(results1)

    logger.info(f"Starting headless Crawl without extension")
    crawled_domains = list(results1.keys())
    results2 = await run_browser(crawled_domains)
    evaluated_results2 = evaluate_requests(results2)

    correlated_results = correlate_results(evaluated_results1, evaluated_results2)

    logger.info(f"Writing results to files")
    write_results(evaluated_results1, "resultsWithExtension.json")
    write_results(evaluated_results2, "resultsWithoutExtension.json")
    write_results(correlated_results, "correlatedResults.json")


if __name__ == "__main__":
    asyncio.run(main())
