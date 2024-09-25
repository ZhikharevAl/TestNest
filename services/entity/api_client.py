import allure

from services.entity.models.entity_model import EntityRequest, EntityResponse
from services.entity.payloads import Payloads

from .http_client import HTTPClient


class APIClient:
    """API client for interacting with the service."""

    def __init__(self, base_url: str) -> None:
        """Initializes the APIClient with a base URL."""
        self.http_client = HTTPClient(base_url)
        self.payloads = Payloads()

    @allure.step("Create entity")
    def create_entity(self) -> str:
        """Creates a new entity and returns its ID."""
        response = self.http_client.post("/api/create", self.payloads.create_entity)
        response.raise_for_status()
        return response.text

    @allure.step("Get entity")
    def get_entity(self, entity_id: str) -> EntityResponse:
        """Gets an entity with the given entity ID."""
        response = self.http_client.get(f"/api/get/{entity_id}")
        response.raise_for_status()
        data = response.json()
        return EntityResponse(**data)

    @allure.step("Get all entities")
    def get_all_entities(
        self,
        title: str | None = None,
        verified: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[EntityResponse]:
        """Gets all entities with the provided filters."""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        response = self.http_client.get("/api/getAll", params=params)
        response.raise_for_status()
        data = response.json()
        entities = data["entity"]
        return [EntityResponse(**item) for item in entities]

    @allure.step("Update entity")
    def update_entity(self, entity_id: str, entity: EntityRequest) -> None:
        """Updates an entity with the given entity ID and data."""
        response = self.http_client.patch(
            f"/api/patch/{entity_id}", entity.model_dump()
        )
        response.raise_for_status()

    @allure.step("Delete entity")
    def delete_entity(self, entity_id: str) -> None:
        """Deletes an entity with the given entity ID."""
        response = self.http_client.delete(f"/api/delete/{entity_id}")
        response.raise_for_status()
