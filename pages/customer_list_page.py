from statistics import mean

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


class CustomerListPage(BasePage):
    """Page object for the Customer List page in XYZ Bank application."""

    URL = "/manager/list"
    EXPECTED_TITLE = "XYZ Bank"

    # Locators
    FIRST_NAME_HEADER: tuple[str, str] = (
        By.XPATH,
        "//a[contains(@ng-click, \"'fName';\")]",
    )

    CUSTOMER_ROWS: tuple[str, str] = (By.XPATH, "//tbody/tr")
    DELETE_BUTTON: tuple[str, str] = (By.XPATH, "//*[text() = 'Delete']")
    SEARCH_CUSTOMER_INPUT: tuple[str, str] = (By.XPATH, "//input[@type='text']")

    def __init__(self, browser: WebDriver) -> None:
        """

        Initialize the CustomerListPage.

        Args:
            browser: WebDriver instance
        """
        super().__init__(
            browser,
            base_url="https://www.globalsqa.com/angularJs-protractor/BankingProject/#",
        )

    def open(self) -> None:
        """Open the Customer List page."""
        self.open_page(self.URL)

    def is_page_loaded(self) -> bool:
        """Check if the page is loaded.

        Returns:
            bool: True if the page is loaded, False otherwise
        """
        return self.get_title() == self.EXPECTED_TITLE and self.is_element_present(
            self.FIRST_NAME_HEADER,
        )

    def click_first_name_header(self) -> None:
        """Click the first name header."""
        self.click_element(self.FIRST_NAME_HEADER)

    def get_customer_names(self) -> list[str]:
        """Get the list of customer first names.

        Returns:
            List[str]: List of customer first names
        """
        customer_rows: list[WebElement] = self.wait_for_elements(self.CUSTOMER_ROWS)
        return [row.find_element(By.XPATH, "./td[1]").text for row in customer_rows]

    @staticmethod
    def sort_names_programmatically(names: list[str]) -> list[str]:
        """Return a list of names sorted alphabetically.

        Args:
            names (List[str]): List of names to sort

        Returns:
            List[str]: Sorted list of names
        """
        return sorted(names)

    @staticmethod
    def get_average_name_length(names: list[str]) -> float:
        """Calculate the average length of customer names."""
        return mean(len(name) for name in names)

    @staticmethod
    def find_name_closest_to_average_length(
        names: list[str],
        average_length: float,
    ) -> str:
        """Find the name with length closest to the average length."""
        return min(names, key=lambda name: abs(len(name) - average_length))

    def search_customer(self, name: str) -> None:
        """Search for a customer by name."""
        self.wait_for_element(self.SEARCH_CUSTOMER_INPUT).send_keys(name)

    def delete_customer(self, name: str) -> None:
        """Delete a customer by name."""
        self.search_customer(name)
        self.click_element(self.DELETE_BUTTON)

    def clear_input(self) -> None:
        """Clear the search input."""
        self.clear_field(self.SEARCH_CUSTOMER_INPUT)

    def find_customer_row_by_name(self, name: str) -> WebElement:
        """Find the row corresponding to the customer name."""
        customer_rows: list[WebElement] = self.wait_for_elements(self.CUSTOMER_ROWS)
        for row in customer_rows:
            first_name_element = self.find_element((By.XPATH, "./td[1]"))
            if first_name_element.text == name:
                return row
        error_message = f"Customer with name '{name}' not found"
        raise ValueError(error_message)
