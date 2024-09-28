import allure
import pytest
from requests import HTTPError

from services.entity.api_client import APIClient
from services.entity.models.entity_model import (
    EntityResponse,
)
from services.entity.models.validators import validate_entity
from services.entity.payloads import Payloads


@allure.epic("Entity Management")
@allure.feature("CRUD Operations")
class TestEntityAPI:
    """Test suite for Entity API CRUD operations."""

    @allure.title("Test create entity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that an entity can be created successfully")
    @pytest.mark.api
    def test_create_entity(self, api_client: APIClient) -> None:
        """Test create entity."""
        with allure.step("Creating a new entity"):
            response = api_client.create_entity()
            id_entity = response.text
            assert (
                response.status_code == 200
            ), f"Error while creating entity: {response.status_code}, {response.text}"

        with allure.step("Checking that a valid entity ID is returned"):
            assert id_entity.isdigit(), f"Expected a numeric ID, got: {id_entity}"

        with allure.step(f"Retrieving the created entity with ID {id_entity}"):
            http_response, entity = api_client.get_entity(id_entity)

        with allure.step("Checking the status code when retrieving the entity"):
            assert http_response.status_code == 200, (
                f"Error while retrieving entity: {http_response.status_code}, "
                f"{http_response.text}"
            )

        validated_entity = validate_entity(entity.model_dump())
        assert str(validated_entity.id) == id_entity, (
            f"Created entity ID does not match: expected {id_entity}, "
            f"got {validated_entity.id}"
        )

    @allure.title("Test get entity")
    @allure.description("Verify that a specific entity can be retrieved")
    @pytest.mark.api
    def test_get_entity(self, api_client: APIClient, entity_id: str) -> None:
        """Test that verifies a specific entity can be retrieved."""
        response, entity = api_client.get_entity(entity_id)
        assert (
            response.status_code == 200
        ), f"Error while retrieving entity: {response.status_code}, {response.text}"

        validate_entity(entity, entity)

    @allure.title("Test get all entities")
    @allure.description("Verify that all entities can be retrieved")
    @pytest.mark.api
    def test_get_all_entities(self, api_client: APIClient) -> None:
        """Test that verifies all entities can be retrieved."""
        with allure.step("Retrieving all entities"):
            response, entities = api_client.get_all_entities()
            assert response.status_code == 200, (
                f"Error while retrieving entities: {response.status_code}, "
                f"{response.text}"
            )

        with allure.step("Checking that a non-empty list is returned"):
            assert entities, "Received an empty list of entities"

        with allure.step("Checking the types of the retrieved objects"):
            assert all(
                isinstance(entity, EntityResponse) for entity in entities
            ), "Not all elements are EntityResponse objects"

        for entity in entities:
            validate_entity(entity)

    @allure.title("Test update entity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that an entity can be updated successfully")
    @pytest.mark.api
    def test_update_entity(self, api_client: APIClient, entity_id: str) -> None:
        """Tests that an entity can be updated."""
        updated_entity_request = Payloads.create_entity_request()

        response, _ = api_client.update_entity(entity_id, updated_entity_request)
        assert (
            response.status_code == 204
        ), f"Expected status 204, got: {response.status_code}"

        with allure.step("Retrieving the updated entity"):
            response, updated_entity = api_client.get_entity(entity_id)

        validate_entity(updated_entity, updated_entity_request)

        assert updated_entity.id == int(
            entity_id
        ), f"ID mismatch: expected {entity_id}, got {updated_entity.id}"

    @allure.title("Test delete entity")
    @allure.description("Verify that an entity can be deleted successfully")
    @pytest.mark.api
    def test_delete_entity(self, api_client: APIClient) -> None:
        """Tests that an entity can be deleted successfully."""
        with allure.step("Creating a new entity"):
            response = api_client.create_entity()
            new_entity_id = response.text
            assert (
                response.status_code == 200
            ), f"Error while creating entity: {response.status_code}, {response.text}"

        with allure.step(f"Deleting the entity with ID {new_entity_id}"):
            delete_response = api_client.delete_entity(new_entity_id)
            assert delete_response.status_code == 204, (
                f"Error while deleting entity: {delete_response.status_code}, "
                f"{delete_response.text}"
            )

        with (
            allure.step(
                f"Attempting to retrieve the deleted entity with ID {new_entity_id}"
            ),
            pytest.raises(HTTPError) as excinfo,
        ):
            api_client.get_entity(new_entity_id)

        with allure.step("Validating the error for the deleted entity retrieval"):
            assert (
                excinfo.value.response.status_code == 500
            ), f"Expected status 500, but got: {excinfo.value.response.status_code}"
            error_message = excinfo.value.response.json().get("error")
            assert error_message == "no rows in result set", (
                f"Expected error message 'no rows in result set', but got: "
                f"{error_message}"
            )

        with allure.step(
            "Retrieving all entities and ensuring the deleted entity is not present"
        ):
            all_response, all_entities = api_client.get_all_entities()
            assert (
                all_response.status_code == 200
            ), f"Error while retrieving all entities: {all_response.status_code}"

            entity_ids = [entity.id for entity in all_entities]
            assert new_entity_id not in entity_ids, (
                f"Deleted entity with ID {new_entity_id} is "
                f"still present among all entities"
            )
