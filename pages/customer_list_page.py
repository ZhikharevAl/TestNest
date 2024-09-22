import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config.config import CUSTOMER_LIST_URL
from pages.base_page import BasePage
from utils import find_name_closest_to_average_length, get_average_name_length


class CustomerListPage(BasePage):
    """Page object for the Customer List page in XYZ Bank application."""

    # Locators
    FIRST_NAME_HEADER: tuple[str, str] = (
        By.XPATH,
        "//a[contains(@ng-click, \"'fName';\")]",
    )

    CUSTOMER_ROWS: tuple[str, str] = (By.XPATH, "//tbody/tr")
    DELETE_BUTTON: tuple[str, str] = (By.XPATH, "//*[text() = 'Delete']")
    SEARCH_CUSTOMER_INPUT: tuple[str, str] = (By.XPATH, "//input[@type='text']")

    def __init__(self, browser: WebDriver) -> None:
        """Initialize the CustomerListPage."""
        super().__init__(browser, url=CUSTOMER_LIST_URL)

    @allure.step("Check if Customer List page is loaded")
    def is_page_loaded(self) -> bool:
        """Check if the page is loaded.

        Returns:
            bool: True if the page is loaded, False otherwise
        """
        return self.is_element_present(self.FIRST_NAME_HEADER)

    @allure.step("Click on the First Name header")
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

    @allure.step("Sort customers by first name")
    def sort_names(self, sort_direction: str) -> None:
        """Sort customers by first name.

        Args:
            sort_direction (str): The direction to sort ('ascending' or 'descending')
        """
        current_order = self.get_customer_names()
        if sort_direction == "descending":
            while current_order == self.get_customer_names():
                self.click_first_name_header()
        elif sort_direction == "ascending":
            while current_order == self.get_customer_names():
                self.click_first_name_header()
                if current_order != self.get_customer_names():
                    self.click_first_name_header()
                    break
        else:
            error_message = "Invalid sort direction. Use 'ascending' or 'descending'."
            raise ValueError(error_message)

    @allure.step("Verify customer sorting")
    def verify_sorting(self, names: list[str]) -> bool:
        """Verify the sorting of customers."""
        return names == sorted(names) or names == sorted(names, reverse=True)

    @allure.step("Search for a customer by name: {name}")
    def search_customer(self, name: str) -> None:
        """Search for a customer by name."""
        self.wait_for_element(self.SEARCH_CUSTOMER_INPUT).send_keys(name)

    @allure.step("Delete customer by name: {name}")
    def delete_customer(self, name: str) -> None:
        """Delete a customer by name."""
        self.search_customer(name)
        self.click_element(self.DELETE_BUTTON)

    @allure.step("Clear the search input")
    def clear_input(self) -> None:
        """Clear the search input."""
        self.clear_field(self.SEARCH_CUSTOMER_INPUT)

    @allure.step("Find the row corresponding to the customer name: {name}")
    def find_customer_row_by_name(self, name: str) -> WebElement:
        """Find the row corresponding to the customer name."""
        customer_rows: list[WebElement] = self.wait_for_elements(self.CUSTOMER_ROWS)
        for row in customer_rows:
            first_name_element = row.find_element(By.XPATH, "./td[1]")
            if first_name_element.text == name:
                return row
        error_message = f"Customer with name '{name}' not found"
        raise ValueError(error_message)

    @allure.step("Delete customer with average name length")
    def delete_customer_with_average_length(self) -> tuple[str, list[str], list[str]]:
        """Delete a customer with an average name length and return information."""
        initial_names = self.get_customer_names()
        if not initial_names:
            error_message = "No customers found"
            raise ValueError(error_message)

        average_length = get_average_name_length(initial_names)
        deleted_name = find_name_closest_to_average_length(
            initial_names, average_length
        )

        self.delete_customer(deleted_name)
        self.clear_input()

        remaining_names = self.get_customer_names()

        return deleted_name, initial_names, remaining_names

    @allure.step("Verify customer deletion")
    def verify_delete(
        self, deleted_name: str, initial_names: list[str], remaining_names: list[str]
    ) -> None:
        """Verify that a customer was successfully deleted.

        Args:
            deleted_name (str): The name of the deleted customer.
            initial_names (List[str]): The list of customer names before deletion.
            remaining_names (List[str]): The list of customer names after deletion.

        Raises:
            AssertionError: If the deletion verification fails.
        """
        assert deleted_name not in remaining_names, (
            f"Customer '{deleted_name}' " f"was not deleted"
        )
        assert (
            len(remaining_names) == len(initial_names) - 1
        ), "Number of customers did not decrease by 1"
