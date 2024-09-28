import allure
import requests
from requests import Response

from services.entity.models.entity_model import EntityRequest, EntityResponse
from services.entity.payloads import Payloads

from .api_endpoints import APIEndpoints
from .http_client import HTTPClient


class APIClient:
    """API client for interacting with the service."""

    def __init__(self, base_url: str) -> None:
        """Initializes the APIClient with a base URL."""
        self.base_url = base_url
        self.http_client = HTTPClient(base_url)
        self.payloads = Payloads()

    @allure.step("Create entity")
    def create_entity(self) -> Response:
        """Creates a new entity and returns its ID."""
        response = self.http_client.post(
            APIEndpoints.CREATE_ENDPOINT, self.payloads.generate_entity_payload()
        )
        response.raise_for_status()
        return response

    @allure.step("Get entity")
    def get_entity(self, entity_id: str) -> tuple[requests.Response, EntityResponse]:
        """Gets an entity with the given entity ID."""
        response = self.http_client.get(f"{APIEndpoints.GET_ENDPOINT}{entity_id}")
        response.raise_for_status()
        data = response.json()
        entity = EntityResponse(**data)
        return response, entity

    @allure.step("Get all entities")
    def get_all_entities(
        self,
        title: str | None = None,
        verified: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> tuple[requests.Response, list[EntityResponse]]:
        """Gets all entities with the provided filters."""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        response = self.http_client.get(APIEndpoints.GET_ALL_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        entities = data["entity"]
        return response, [EntityResponse(**item) for item in entities]

    @allure.step("Update entity")
    def update_entity(
        self, entity_id: str, entity: EntityRequest
    ) -> tuple[requests.Response, EntityResponse | None]:
        """Updates an entity with the given entity ID and data."""
        response = self.http_client.patch(
            f"{APIEndpoints.UPDATE_ENDPOINT}{entity_id}", entity.model_dump()
        )
        response.raise_for_status()
        if response.status_code == 204:
            return response, None
        data = response.json()
        entity = EntityResponse(**data)
        return response, entity

    @allure.step("Delete entity")
    def delete_entity(self, entity_id: str) -> requests.Response:
        """Deletes an entity with the given entity ID."""
        with allure.step(f"Sending request to delete entity with ID {entity_id}"):
            response = self.http_client.delete(
                f"{APIEndpoints.DELETE_ENDPOINT}{entity_id}"
            )

        with allure.step("Verifying successful entity deletion"):
            if response.status_code == 204:
                allure.attach(
                    f"Entity with ID {entity_id} successfully deleted",
                    name="Entity Deletion",
                )
            else:
                allure.attach(
                    f"Error deleting entity with ID {entity_id}: {response.text}",
                    name="Deletion Error",
                )
        response.raise_for_status()

        return response
