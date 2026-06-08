import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright
from utilities import configReader

@pytest.fixture(params=["chrome"],scope="function")
def browser(request):

    browser_type = request.param

    with sync_playwright() as p:
        if browser_type == "chrome":
            browser = p.chromium.launch(headless=False)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=False)
        else:
            raise ValueError(f"Unsupported browser : {browser_type}")
        yield browser
        browser.close()

@pytest.fixture(autouse=True)
def setup_function(page):
    page.goto(configReader.readConfig("basic info","testsiteurl"))

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(record_video_dir="videos/")
    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    global page
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page
    page.wait_for_timeout(2000)
    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path="trace.zip")
    page.close()
    context.close()

@pytest.fixture()
def log_on_failure(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(page.screenshot(path="screenshot/fullpage.png"), name="failurescreenshot",
                      attachment_type=AttachmentType.PNG)