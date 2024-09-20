import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from data.generators import create_customers
from pages.add_customer_page import AddCustomerPage


@allure.epic("Customer Management")
@allure.feature("Add Customer")
@allure.description_html("""
<h2>Testing Customer Registration in XYZ Bank</h2>
<p>This test suite verifies the functionality of adding customer
            to the XYZ Bank system, including:</p>
<ul>
    <li>Generating test data for customer</li>
    <li>Opening the Add Customer page</li>
    <li>For each customer:</li>
    <ul>
        <li>Filling in the customer information (First Name, Last Name, Post Code)</li>
        <li>Submitting the registration form</li>
        <li>Verifying the success message</li>
        <li>Accepting the alert</li>
    </ul>
    <li>Verifying that customer were added successfully</li>
</ul>
<p>The test uses specially generated data where:</p>
<ul>
    <li>Post Code is a 10-digit number</li>
    <li>First Name is generated based on the Post Code</li>
    <li>Last Name is randomly generated</li>
</ul>
""")
class TestAddCustomer:
    """
    A test class for verifying the addition of a new customer with valid data.

    This class contains a test that ensures a new customer can be added
    with valid data through the customer management system.

    Methods:
        test_add_customer(browser: WebDriver) -> None:
            Test adding a new customer with valid data.
    """

    @allure.story("Add a new customer with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_customer(self, browser: WebDriver) -> None:
        """
        Add a new customer with valid data.

        This test verifies the functionality of adding a new customer
        with valid data to the customer management system.

        Args:
            browser (WebDriver): The Selenium WebDriver instance.

        Returns:
            None
        """
        with allure.step("Generate customer data"):
            customer = create_customers(1)[0]

        with allure.step("Open Add Customer page"):
            customer_page = AddCustomerPage(browser)
            customer_page.open()

        with allure.step("Verify page is loaded"):
            assert customer_page.is_page_loaded(), "Add Customer page is not loaded"

        with allure.step("Fill customer information"):
            customer_page.add_customer(
                customer.first_name,
                customer.last_name,
                customer.post_code,
            )

        allure.attach(
            browser.get_screenshot_as_png(),
            name="add_customer_result",
            attachment_type=allure.attachment_type.PNG,
        )

        with allure.step("Submit customer information"):
            customer_page.click_add_customer()

        with allure.step("Verify success message"):
            alert_text = customer_page.get_alert_text()
            assert (
                "Customer added successfully" in alert_text
            ), f"Unexpected alert message: {alert_text}"

        with allure.step("Accept alert"):
            customer_page.accept_alert()
