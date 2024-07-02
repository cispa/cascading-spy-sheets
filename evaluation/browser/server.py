from flask import Flask, request
import json
import traceback
from datetime import datetime
from user_agent_parser import Parser

CONFIG = {"port": 3000}
tor_user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0"

app = Flask(__name__)


def user_agent_to_file_name(user_agent):
    parser = Parser(user_agent)
    browser, release, os, _, _, _, _ = parser()
    is_tor = user_agent == tor_user_agent
    result = f"{browser if not is_tor else 'tor'}_{release}_{os}"
    return result


@app.route('/<path:path>')
def index(path):
    if ".." in path or path.startswith("/"):
        return "Invalid path", 400

    if not path.endswith(".html"):
        path = path + ".html"

    return app.send_static_file(path)


@app.route("/report/full", methods=["POST"])
def report_full():
    timestamp = datetime.now()
    formatted_time = timestamp.strftime("%Y-%m-%d-%H-%M")
    try:
        experiment = request.args.get("experiment", "")
        assert experiment != ""
        host = request.args.get("host", "")
        assert host != ""
        os = request.args.get("os", "")
        assert os != ""
        browser = request.args.get("browser", "")
        assert browser != ""
        release = request.args.get("release", "")
        assert release != ""
    except AssertionError:
        e = "Missing query parameters"
        print(e)
        return e, 500
    user_agent = request.headers.get("User-Agent", "")

    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        try:
            data = request.json
            if not "meta" in data:
                data = {"results": data}
                data["meta"] = {
                    "experiment": experiment,
                    "host": host,
                    "os": os,
                    "browser": browser,
                    "release": release,
                    "timestamp": formatted_time,
                    "user_agent": user_agent,
                }
            with open(
                f"report_{experiment}_{host}_{os}_{browser}_{release}.json",
                "w",
            ) as f:
                json.dump(data, f)
            return "success", 200
        except:
            e = traceback.format_exc()
            print(e)
            return e, 500
    elif content_type == "text/plain":
        try:
            data = request.data
            with open(
                f"report_{experiment}_{host}_{os}_{browser}_{release}.json",
                "w",
            ) as f:
                f.write(data.decode())
            return "success", 200
        except:
            e = traceback.format_exc()
            print(e)
            return e, 500
    else:
        e = "Unsupported content type"
        print(e)
        return e, 500


@app.route("/report/create", methods=["POST"])
def report_create():
    timestamp = datetime.now()
    formatted_time = timestamp.strftime("%Y-%m-%d-%H-%M")
    try:
        experiment = request.args.get("experiment", "")
        assert experiment != ""
        host = request.args.get("host", "")
        assert host != ""
        os = request.args.get("os", "")
        assert os != ""
        browser = request.args.get("browser", "")
        assert browser != ""
        release = request.args.get("release", "")
        assert release != ""
    except AssertionError:
        e = "Missing query parameters"
        print(e)
        return e, 500
    user_agent = request.headers.get("User-Agent", "")
    try:
        f = open(
            f"report_{experiment}_{host}_{os}_{browser}_{release}.txt",
            "w",
        )
        f.writelines([host, os, browser, release, formatted_time, user_agent])
        f.close()
        return "success", 200
    except:
        e = traceback.format_exc()
        print(e)
        return e, 500


@app.route("/report/append", methods=["POST"])
def report_append():
    try:
        experiment = request.args.get("experiment", "")
        assert experiment != ""
        host = request.args.get("host", "")
        assert host != ""
        os = request.args.get("os", "")
        assert os != ""
        browser = request.args.get("browser", "")
        assert browser != ""
        release = request.args.get("release", "")
        assert release != ""
    except AssertionError:
        e = "Missing query parameters"
        print(e)
        return e, 500
    try:
        data = request.data
        with open(
            f"report_{experiment}_{host}_{os}_{browser}_{release}.txt",
            "a",
        ) as f:
            f.write(f"{data.decode()}\n")
        return "success", 200
    except:
        e = traceback.format_exc()
        print(e)
        return e, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG["port"])
