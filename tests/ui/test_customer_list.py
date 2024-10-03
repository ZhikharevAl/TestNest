import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.customer_list_page import CustomerListPage


@allure.epic("Customer Management")
@allure.feature("Customer List")
@allure.description_html("""
<h2>Testing Customer List in XYZ Bank</h2>
<p>This test suite verifies the functionality of the customer list
   in the XYZ Bank system, including:</p>
<ul>
    <li>Opening the Customer List page</li>
    <li>Verifying the page is loaded</li>
    <li>Sorting customers by first name in descending order (one click)</li>
    <li>Sorting customers by first name in ascending order (two clicks)</li>
    <li>Comparing programmatically sorted names with UI-sorted names</li>
</ul>
""")
class TestCustomerList:
    """A test class for sort functionality of the customer list in the XYZ Bank."""

    @allure.story("Sort customers by first name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.parametrize("sort_direction", ["descending", "ascending"])
    def test_sort_customers_by_first_name(
        self, browser: WebDriver, sort_direction: str
    ) -> None:
        """Test sorting customers by first name in the specified order."""
        self.customer_list_page = CustomerListPage(browser)
        self.customer_list_page.open_page()
        assert (
            self.customer_list_page.is_page_loaded()
        ), "Customer List page is not loaded"
        self.customer_list_page.sort_names(sort_direction)
        sorted_names = self.customer_list_page.get_customer_names()
        assert self.customer_list_page.verify_sorting(
            sorted_names
        ), f"Customer list is not sorted correctly in {sort_direction} order"
