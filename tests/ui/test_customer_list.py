import allure
import pytest
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
    @allure.story("Sort customers by first name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.parametrize("sort_direction", ["descending", "ascending"])
    def test_sort_customers_by_first_name(self, browser, sort_direction):
        with allure.step("Open Customer List page"):
            customer_list_page = CustomerListPage(browser)
            customer_list_page.open()

        with allure.step("Verify page is loaded"):
            assert (
                customer_list_page.is_page_loaded()
            ), "Customer List page is not loaded"

        with allure.step(f"Sort customers by first name in {sort_direction} order"):
            initial_names = customer_list_page.get_customer_names()

            programmatically_sorted_names = (
                customer_list_page.sort_names_programmatically(initial_names)
            )

            if sort_direction == "descending":
                programmatically_sorted_names = programmatically_sorted_names[::-1]
                customer_list_page.click_first_name_header()
            else:
                customer_list_page.click_first_name_header()
                customer_list_page.click_first_name_header()

            ui_sorted_names = customer_list_page.get_customer_names()

            assert (
                programmatically_sorted_names == ui_sorted_names
            ), f"Customer list is not sorted correctly in {sort_direction} order"

        allure.attach(
            browser.get_screenshot_as_png(),
            name=f"final_sorted_customer_list_{sort_direction}",
            attachment_type=allure.attachment_type.PNG,
        )