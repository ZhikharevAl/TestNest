from typing import Any

import requests

from utils.allure_utils import AllureUtils


class HTTPClient:
    """HTTP client for making requests to a specified base URL."""

    def __init__(self, base_url: str) -> None:
        """Initializes the HTTPClient with a base URL."""
        self.base_url = base_url

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> requests.Response:
        """Sends a GET request to the specified endpoint with the provided data."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        AllureUtils.attach_response(response)
        return response

    def post(self, endpoint: str, data: dict[str, Any]) -> requests.Response:
        """Sends a POST request to the specified endpoint with the provided data."""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=10)
        AllureUtils.attach_response(response)
        return response

    def patch(self, endpoint: str, data: dict[str, Any]) -> requests.Response:
        """Sends a PATCH request to the specified endpoint with the provided data."""
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, json=data, timeout=10)
        AllureUtils.attach_response(response)
        return response

    def delete(self, endpoint: str) -> requests.Response:
        """Sends a DELETE request to the specified endpoint."""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, timeout=10)
        AllureUtils.attach_response(response)
        return response
