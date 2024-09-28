import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def verify_customer_addition(browser: WebDriver) -> None:
    """Verify the success message after adding a customer."""
    alert_text = get_alert_text(browser)
    assert (
        "Customer added successfully" in alert_text
    ), f"Unexpected alert message: {alert_text}"
    accept_alert(browser)

    allure.attach(
        f"Alert Text: {alert_text}",
        name="customer_addition_result",
        attachment_type=allure.attachment_type.TEXT,
    )


def get_alert_text(browser: WebDriver) -> str:
    """Get the text of the alert.

    Args:
        browser: The WebDriver instance.

    Returns:
        str: The text of the alert.
    """
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    return alert.text


def accept_alert(browser: WebDriver) -> None:
    """Accept the alert.

    Args:
        browser: The WebDriver instance.
    """
    alert = browser.switch_to.alert
    alert.accept()
