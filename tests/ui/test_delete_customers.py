import allure
import pytest
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
    @allure.story("Delete customer with average name length")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_delete_customer_with_average_name_length(self, browser):
        with allure.step("Open Customer List page"):
            customer_list_page = CustomerListPage(browser)
            customer_list_page.open()

        with allure.step("Verify page is loaded"):
            assert (
                customer_list_page.is_page_loaded()
            ), "Customer List page is not loaded"

        with allure.step("Get initial customer names"):
            initial_names = customer_list_page.get_customer_names()
            assert len(initial_names) > 0, "No customers found"

        with allure.step("Delete customer with average name length"):
            average_length = customer_list_page.get_average_name_length(initial_names)
            deleted_name = customer_list_page.find_name_closest_to_average_length(
                initial_names, average_length
            )
            customer_list_page.delete_customer(deleted_name)

        with allure.step("Clear input"):
            customer_list_page.clear_input()

        with allure.step("Verify customer was deleted"):
            remaining_names = customer_list_page.get_customer_names()
            assert (
                deleted_name not in remaining_names
            ), f"Customer '{deleted_name}' was not deleted"
            assert (
                len(remaining_names) == len(initial_names) - 1
            ), "Number of customers did not decrease by 1"

        allure.attach(
            browser.get_screenshot_as_png(),
            name="customer_list_after_deletion",
            attachment_type=allure.attachment_type.PNG,
        )
