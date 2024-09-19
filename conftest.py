import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure


@pytest.fixture(scope="function")
def browser(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver


@pytest.fixture(scope="function", autouse=True)
def setup_teardown(request, browser):
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
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
