from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base class to initialize the base page that will be called from all pages."""

    def __init__(self, browser: WebDriver, base_url: str = "") -> None:
        """Initialize the base page with the given browser and base URL.

        Args:
            browser (WebDriver): The Selenium WebDriver instance.
            base_url (str, optional): The base URL of the application. Defaults to "".
        """
        self.browser = browser
        self.base_url = base_url
        self.timeout = 10

    def open_page(self, url: str = "") -> None:
        """Open a page using the given URL.

        Args:
            url (str, optional): The URL to open. If not provided, opens the base URL.
        """
        self.browser.get(f"{self.base_url}{url}")

    def get_title(self) -> str:
        """Get the title of the current page.

        Returns:
            str: The title of the current page.
        """
        return self.browser.title

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """Find an element on the page.

        Args:
            locator (Tuple[str, str]): The locator of
            the element (e.g., (By.ID, "example")).

        Returns:
            WebElement: The found element.

        Raises:
            NoSuchElementException: If the element is not found.
        """
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException as e:
            error_message = f"Element not found with locator: {locator}"
            raise NoSuchElementException(error_message) from e

    def click_element(self, locator: tuple[str, str]) -> None:
        """Click on an element.

        Args:
            locator (Tuple[str, str]): The locator of the element to click.
        """
        element = self.find_element(locator)
        element.click()

    def enter_text(self, locator: tuple[str, str], text: str) -> None:
        """Enter text into an input field.

        Args:
            locator (Tuple[str, str]): The locator of the input field.
            text (str): The text to enter.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator: tuple[str, str]) -> bool:
        """Check if an element is present on the page.

        Args:
            locator (Tuple[str, str]): The locator of the element.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            self.find_element(locator)
        except NoSuchElementException:
            return False
        else:
            return True

    def wait_for_element(
        self,
        locator: tuple[str, str],
        timeout: int | None = None,
    ) -> WebElement:
        """Wait for an element to be present on the page.

        Args:
            locator (Tuple[str, str]): The locator of the element to wait for.
            timeout (int, optional): The maximum time to wait. Defaults to self.timeout.

        Returns:
            WebElement: The found element.

        Raises:
            TimeoutException: If the element is not found within the specified timeout.
        """
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
        self,
        locator: tuple[str, str],
        timeout: int | None = None,
    ) -> list[WebElement]:
        """Wait for multiple elements to be present on the page.

        Args:
            locator (Tuple[str, str]): The locator of the elements to wait for.
            timeout (int, optional): The maximum time to wait. Defaults to self.timeout.

        Returns:
            List[WebElement]: The found elements.

        Raises:
            TimeoutException: If the elements are not found within the specified
            timeout.
        """
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
        """Clear the field specified by the locator.

        Args:
            locator (Tuple[str, str]): Locator for the input field (By, locator string)
        """
        element = self.wait_for_element(locator)
        element.clear()
