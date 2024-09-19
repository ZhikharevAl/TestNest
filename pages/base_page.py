from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, Any, List


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, browser, base_url: str = ""):
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

    def find_element(self, locator: Tuple[str, str]) -> Any:
        """Find an element on the page.

        Args:
            locator (Tuple[str, str]): The locator of the
             element (e.g., (By.ID, "example")).

        Returns:
            WebElement: The found element.

        Raises:
            NoSuchElementException: If the element is not found.
        """
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException as e:
            raise NoSuchElementException(
                f"Element not found with locator: " f"{locator}"
            ) from e

    def click_element(self, locator: Tuple[str, str]) -> None:
        """Click on an element.

        Args:
            locator (Tuple[str, str]): The locator of the element to click.
        """
        element = self.find_element(locator)
        element.click()

    def enter_text(self, locator: Tuple[str, str], text: str) -> None:
        """Enter text into an input field.

        Args:
            locator (Tuple[str, str]): The locator of the input field.
            text (str): The text to enter.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if an element is present on the page.

        Args:
            locator (Tuple[str, str]): The locator of the element.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element(self, locator: Tuple[str, str], timeout: int = None) -> Any:
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
                EC.presence_of_element_located(locator)
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"Element not found within {timeout} " f"seconds. Locator: {locator}"
            ) from e

    def wait_for_elements(
        self, locator: Tuple[str, str], timeout: int = None
    ) -> List[WebElement]:
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
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException as e:
            raise TimeoutException(
                f"Elements not found within {timeout} seconds. Locator: {locator}"
            ) from e

    def clear_field(self, locator: tuple) -> None:
        """Clear the field specified by the locator.

        Args:
            locator (tuple): Locator for the input field (By, locator string)
        """
        element = self.wait_for_element(locator)
        element.clear()
