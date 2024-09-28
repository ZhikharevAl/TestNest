import json

import allure
from allure_commons.types import AttachmentType
from requests import Response


class AllureUtils:
    """Utility class for attaching API responses to Allure reports."""

    @staticmethod
    def attach_response(response: Response) -> None:
        """Attach the details of an API response to an Allure report."""
        try:
            response_json = response.json()
            formatted_response = json.dumps(response_json, indent=4)
        except json.JSONDecodeError:
            formatted_response = response.text or "Empty response"

        allure.attach(
            body=formatted_response,
            name="API Response",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=str(response.status_code),
            name="Status Code",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=str(response.headers),
            name="Headers",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=str(response.url),
            name="URL",
            attachment_type=AttachmentType.TEXT,
        )
