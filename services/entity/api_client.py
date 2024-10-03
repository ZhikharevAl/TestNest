import allure
from requests import Response

from .api_endpoints import APIEndpoints
from .http_client import HTTPClient


class APIClient:
    """Low-level API client for interacting with the service."""

    def __init__(self, base_url: str) -> None:
        """Initializes the APIClient with a base URL."""
        self.base_url = base_url
        self.http_client = HTTPClient(base_url)

    @allure.step("Create entity")
    def create_entity(self, payload: dict) -> Response:
        """Creates a new entity."""
        return self.http_client.post(APIEndpoints.CREATE_ENDPOINT, payload)

    @allure.step("Get entity")
    def get_entity(self, entity_id: str) -> Response:
        """Gets an entity with the given entity ID."""
        return self.http_client.get(f"{APIEndpoints.GET_ENDPOINT}{entity_id}")

    @allure.step("Get all entities")
    def get_all_entities(self, params: dict | None = None) -> Response:
        """Gets all entities with the provided filters."""
        return self.http_client.get(APIEndpoints.GET_ALL_ENDPOINT, params=params)

    @allure.step("Update entity")
    def update_entity(self, entity_id: str, payload: dict) -> Response:
        """Updates an entity with the given entity ID and data."""
        return self.http_client.patch(
            f"{APIEndpoints.UPDATE_ENDPOINT}{entity_id}", payload
        )

    @allure.step("Delete entity")
    def delete_entity(self, entity_id: str) -> Response:
        """Deletes an entity with the given entity ID."""
        return self.http_client.delete(f"{APIEndpoints.DELETE_ENDPOINT}{entity_id}")
