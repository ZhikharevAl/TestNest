import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.customer_list_page import CustomerListPage


@allure.epic("Customer Management")
@allure.feature("Delete Customer")
@allure.description_html("""
<h2>Testing Customer Deletion in XYZ Bank</h2>
<p>This test verifies the functionality of deleting a customer
   from the XYZ Bank system based on average name length, including:</p>
<ul>
    <li>Opening the Customer List page</li>
    <li>Verifying the page is loaded</li>
    <li>Getting the list of customer names</li>
    <li>Calculating the average name length</li>
    <li>Finding the name closest to the average length</li>
    <li>Deleting the customer with that name</li>
    <li>Clearing the search input field</li>
    <li>Verifying the customer was deleted</li>
</ul>
""")
class TestDeleteCustomer:
    """A class for verifying the deletion of a customer with an average name length."""

    @allure.story("Delete customer with average name length")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_delete_customer_with_average_name_length(self, browser: WebDriver) -> None:
        """Test deleting a customer with an average name length."""
        self.customer_list_page = CustomerListPage(browser)
        self.customer_list_page.open_page()
        assert self.customer_list_page.is_page_loaded(), (
            "Customer List page " "is not loaded"
        )
        deleted_name, initial_names, remaining_names = (
            self.customer_list_page.delete_customer_with_average_length()
        )
        self.customer_list_page.verify_delete(
            deleted_name, initial_names, remaining_names
        )
