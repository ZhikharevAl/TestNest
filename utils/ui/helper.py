import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Helper:
    """A helper class for managing WebDriver interactions and verifications."""

    def __init__(self, browser: WebDriver) -> None:
        """Initialize the Helper class."""
        self.browser = browser

    def verify_customer_addition(self) -> None:
        """Verify the success message after adding a customer."""
        alert_text = self.get_alert_text()
        assert (
            "Customer added successfully" in alert_text
        ), f"Unexpected alert message: {alert_text}"
        self.accept_alert()

        allure.attach(
            f"Alert Text: {alert_text}",
            name="customer_addition_result",
            attachment_type=allure.attachment_type.TEXT,
        )

    def get_alert_text(self) -> str:
        """Get the text of the alert."""
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        return alert.text

    def accept_alert(self) -> None:
        """Accept the alert."""
        alert = self.browser.switch_to.alert
        alert.accept()

    def wait_for_alert(self, timeout: int = 10) -> None:
        """Wait for an alert to be present."""
        WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
