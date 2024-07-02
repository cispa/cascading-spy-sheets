from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import traceback
import platform
import time
import sys

if len(sys.argv) < 2:
    print("Please provide a url.")
    sys.exit(-1)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(sys.argv[1], timeout=60 * 1000, wait_until="commit")
    time.sleep(120)
    browser.close()