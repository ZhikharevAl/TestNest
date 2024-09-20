import allure
import pytest
from _pytest.reports import TestReport
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture
def browser() -> WebDriver:
    """
    Fixture to initialize and provide a WebDriver instance.

    Returns:
        WebDriver: The WebDriver instance for the browser.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


@pytest.fixture(autouse=True)
def setup_teardown(request: pytest.FixtureRequest, browser: WebDriver) -> None:
    """
    Fixture to set up and tear down the test environment.

    Args:
        request (pytest.FixtureRequest): The fixture request object.
        browser (WebDriver): The WebDriver instance for the browser.
    """
    allure.dynamic.parameter("browser", browser.capabilities["browserName"])
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(
            browser.get_screenshot_as_png(),
            name=f"screenshot_{item.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            "\n".join(browser.get_log("browser")),
            name="browser_logs",
            attachment_type=allure.attachment_type.TEXT,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> TestReport:
    """
    Hook to add additional information to the test report.

    This hook is called after each test is run to modify the test report.
    It can be used to add custom information to the report.

    Args:
        item (pytest.Item): The test item that was run.

    Returns:
        TestReport: The test report for the test item.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
