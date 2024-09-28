import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from data.generators import create_customers
from pages.add_customer_page import AddCustomerPage
from utils.ui.helper import verify_customer_addition


@allure.epic("Customer Management")
@allure.feature("Add Customer")
@allure.description_html("""
<h2>Testing Customer Registration in XYZ Bank</h2>
<p>This test suite verifies the functionality of adding customer
            to the XYZ Bank system, including:</p>
<ul>
    <li>Generating test data for customer</li>
    <li>Opening the Add Customer page</li>
    <li>Filling in the customer information (First Name, Last Name, Post Code)</li>
    <li>Submitting the registration form</li>
    <li>Verifying the success message</li>
    <li>Accepting the alert</li>
</ul>
<p>The test uses specially generated data where:</p>
<ul>
    <li>Post Code is a 10-digit number</li>
    <li>First Name is generated based on the Post Code</li>
    <li>Last Name is randomly generated</li>
</ul>
""")
class TestAddCustomer:
    """Tests for adding a new customer."""

    @allure.story("Add a new customer with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_customer(self, browser: WebDriver) -> None:
        """Test adding a new customer with valid data."""
        self.customer = create_customers(1)[0]
        self.customer_page = AddCustomerPage(browser)
        self.customer_page.open_page()
        assert (
            self.customer_page.is_page_loaded()
        ), "The page for adding customers has not been opened"
        self.customer_page.add_customer(
            self.customer.first_name,
            self.customer.last_name,
            self.customer.post_code,
        )
        verify_customer_addition(browser)
