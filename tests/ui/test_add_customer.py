import allure
import pytest

from data.generators import create_customers
from pages.add_customer_page import AddCustomerPage
from utils.ui.helper import Helper


@allure.epic("Customer Management")
@allure.feature("Add Customer")
@allure.description_html("""
<h2>Testing Customer Registration in XYZ Bank</h2>
<p>This test suite verifies the functionality of adding customers
            to the XYZ Bank system, including:</p>
<ul>
    <li>Generating test data for customers</li>
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
    def test_add_customer(
        self, add_customer_page: AddCustomerPage, helper: Helper
    ) -> None:
        """Test adding a new customer with valid data."""
        customer = create_customers(1)[0]
        add_customer_page.open_page()

        assert (
            add_customer_page.is_page_loaded()
        ), "The page for adding customers has not been opened"

        add_customer_page.add_customer(
            customer.first_name,
            customer.last_name,
            customer.post_code,
        )

        helper.wait_for_alert()
        helper.verify_customer_addition()
