import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config_ui.config import BASE_URL, DEFAULT_TIMEOUT


class BasePage:
    """Base class to initialize the base page that will be called from all pages."""

    def __init__(self, browser: WebDriver, url: str = "") -> None:
        """Initialize the base page with the given browser and base URL."""
        self.browser = browser
        self.base_url = BASE_URL
        self.url = url
        self.timeout = DEFAULT_TIMEOUT

    def open_page(self) -> None:
        """Open a page using the given URL."""
        with allure.step(f"Opening page: {self.base_url}{self.url}"):
            self.browser.get(f"{self.base_url}{self.url}")

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """Find an element on the page."""
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException as e:
            error_message = f"Element not found with locator: {locator}"
            raise NoSuchElementException(error_message) from e

    def click_element(self, locator: tuple[str, str]) -> None:
        """Click on an element."""
        with allure.step(f"Clicking element with locator: {locator}"):
            element = self.find_element(locator)
            element.click()

    def enter_text(self, locator: tuple[str, str], text: str) -> None:
        """Enter text into an input field."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator: tuple[str, str]) -> bool:
        """Check if an element is present on the page."""
        try:
            self.find_element(locator)
        except NoSuchElementException:
            return False
        else:
            return True

    def wait_for_element(
        self, locator: tuple[str, str], timeout: int | None = None
    ) -> WebElement:
        """Wait for an element to be present on the page."""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(locator),
            )
        except TimeoutException as e:
            error_message = (
                f"Element not found within {timeout} seconds. Locator: {locator}"
            )
            raise TimeoutException(error_message) from e

    def wait_for_elements(
        self, locator: tuple[str, str], timeout: int | None = None
    ) -> list[WebElement]:
        """Wait for multiple elements to be present on the page."""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.presence_of_all_elements_located(locator),
            )
        except TimeoutException as e:
            error_message = (
                f"Elements not found within {timeout} seconds. Locator: {locator}"
            )
            raise TimeoutException(error_message) from e

    def clear_field(self, locator: tuple[str, str]) -> None:
        """Clear the field specified by the locator."""
        element = self.wait_for_element(locator)
        element.clear()
