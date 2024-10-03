from requests import Response

from services.entity.api_client import APIClient
from services.entity.models.entity_model import EntityRequest, EntityResponse
from services.entity.payloads import Payloads


class EntityService:
    """High-level service for entity operations with deserialization."""

    def __init__(self, api_client: APIClient) -> None:
        """Initializes the service with the provided API client."""
        self.api_client = api_client
        self.payloads = Payloads()

    def create_entity(self) -> tuple[Response, EntityResponse]:
        """Creates a new entity and returns its data."""
        payload = self.payloads.generate_entity_payload()
        response = self.api_client.create_entity(payload)
        response.raise_for_status()
        entity_id = response.text
        return response, self.get_entity(entity_id)[1]

    def get_entity(self, entity_id: str) -> tuple[Response, EntityResponse]:
        """Gets an entity with the given entity ID."""
        response = self.api_client.get_entity(entity_id)
        response.raise_for_status()
        data = response.json()
        entity = EntityResponse(**data)
        return response, entity

    def get_all_entities(
        self,
        title: str | None = None,
        verified: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> tuple[Response, list[EntityResponse]]:
        """Gets all entities with the provided filters."""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        response = self.api_client.get_all_entities(params)
        response.raise_for_status()
        data = response.json()
        entities = data["entity"]
        return response, [EntityResponse(**item) for item in entities]

    def update_entity(
        self, entity_id: str, entity: EntityRequest
    ) -> tuple[Response, EntityResponse | None]:
        """Updates an entity with the given entity ID and data."""
        response = self.api_client.update_entity(entity_id, entity.model_dump())
        response.raise_for_status()
        if response.status_code == 204:
            return response, None
        return response, self.get_entity(entity_id)[1]

    def delete_entity(self, entity_id: str) -> Response:
        """Deletes an entity with the given entity ID."""
        response = self.api_client.delete_entity(entity_id)
        response.raise_for_status()
        return response
