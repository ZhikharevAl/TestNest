import allure
import pytest
from requests import HTTPError

from services.entity.api_client import APIClient
from services.entity.models.entity_model import (
    EntityResponse,
)
from services.entity.payloads import Payloads


@allure.epic("Entity Management")
@allure.feature("CRUD Operations")
class TestEntityAPI:
    """Test suite for Entity API CRUD operations."""

    @allure.title("Test create entity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that an entity can be created successfully")
    @allure.step("Create a new entity {entity_id}")
    @pytest.mark.api
    def test_create_entity(self, entity_id: str) -> None:
        """Tests that a new entity can be created successfully."""
        assert entity_id.isdigit()

    @allure.title("Test get entity")
    @allure.description("Verify that a specific entity can be retrieved")
    @pytest.mark.api
    def test_get_entity(self, api_client: APIClient, entity_id: str) -> None:
        """Tests that a specific entity can be retrieved successfully."""
        entity = api_client.get_entity(entity_id)
        assert isinstance(entity, EntityResponse)
        assert str(entity.id) == entity_id

    @allure.title("Test get all entities")
    @allure.description("Verify that all entities can be retrieved")
    @pytest.mark.api
    def test_get_all_entities(self, api_client: APIClient) -> None:
        """Tests that all entities can be retrieved successfully."""
        entities = api_client.get_all_entities()
        assert isinstance(entities, list)
        assert all(isinstance(entity, EntityResponse) for entity in entities)

    @allure.title("Test update entity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that an entity can be updated successfully")
    @pytest.mark.api
    def test_update_entity(self, api_client: APIClient, entity_id: str) -> None:
        """Tests that an entity can be updated successfully."""
        updated_entity = Payloads.create_entity_request()
        api_client.update_entity(entity_id, updated_entity)
        retrieved_entity = api_client.get_entity(entity_id)

        assert retrieved_entity == api_client.get_entity(entity_id)

    @allure.title("Test delete entity")
    @allure.description("Verify that an entity can be deleted successfully")
    @pytest.mark.api
    def test_delete_entity(self, api_client: APIClient) -> None:
        """Tests that an entity can be deleted successfully."""
        new_entity_id = api_client.create_entity()
        api_client.delete_entity(new_entity_id)
        with pytest.raises(HTTPError) as excinfo:
            api_client.get_entity(new_entity_id)
        assert excinfo.value.response.status_code == 500
