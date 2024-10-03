import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import ADD_CUSTOMER_URL
from pages.base_page import BasePage


class AddCustomerPage(BasePage):
    """Page object for the Add Customer page in XYZ Bank application."""

    # Locators
    FIRST_NAME_INPUT: tuple[str, str] = (By.XPATH, '//input[@ng-model="fName"]')
    LAST_NAME_INPUT: tuple[str, str] = (By.XPATH, '//input[@ng-model="lName"]')
    POST_CODE_INPUT: tuple[str, str] = (By.XPATH, '//input[@ng-model="postCd"]')
    ADD_CUSTOMER_BUTTON: tuple[str, str] = (By.XPATH, '//button[@type="submit"]')

    def __init__(self, browser: WebDriver) -> None:
        """Initialize the AddCustomerPage."""
        super().__init__(browser, url=ADD_CUSTOMER_URL)

    @allure.step("Check if Add Customer page is loaded")
    def is_page_loaded(self) -> bool:
        """Check if the page is loaded.

        Returns:
            bool: True if the page is loaded, False otherwise
        """
        return self.is_element_present(self.ADD_CUSTOMER_BUTTON)

    def enter_first_name(self, first_name: str) -> None:
        """Enter the first name in the input field.

        Args:
            first_name (str): First name to enter
        """
        self.wait_for_element(self.FIRST_NAME_INPUT)
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name: str) -> None:
        """Enter the last name in the input field.

        Args:
            last_name (str): Last name to enter
        """
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def enter_post_code(self, post_code: str) -> None:
        """Enter the post code in the input field.

        Args:
            post_code (str): Post code to enter
        """
        self.enter_text(self.POST_CODE_INPUT, post_code)

    @allure.step("Click Add Customer button")
    def click_add_customer(self) -> None:
        """Click the Add Customer button."""
        self.click_element(self.ADD_CUSTOMER_BUTTON)

    @allure.step("Add customer")
    def add_customer(self, first_name: str, last_name: str, post_code: str) -> None:
        """Add a new customer.

        Args:
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            post_code (str): Customer's post code
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_post_code(post_code)
        self.click_add_customer()

    @allure.step("Get alert text")
    def get_alert_text(self) -> str:
        """Get the text of the alert.

        Returns:
            str: The text of the alert
        """
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        return alert.text

    @allure.step("Accept alert")
    def accept_alert(self) -> None:
        """Accept the alert."""
        alert = self.browser.switch_to.alert
        alert.accept()
