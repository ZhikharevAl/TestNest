import allure
import pytest
from requests import HTTPError

from services.entity.entity_service import EntityService
from services.entity.models.entity_model import EntityResponse
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
    def test_create_entity(
        self, entity_service: EntityService, new_entity: EntityResponse
    ) -> None:
        """Test create entity."""
        with allure.step(f"Verifying the created entity with ID {new_entity.id}"):
            assert isinstance(
                new_entity.id, int
            ), f"Expected a numeric ID, got: {new_entity.id}"

            response, fetched_entity = entity_service.get_entity(str(new_entity.id))
            assert (
                response.status_code == 200
            ), f"Error while retrieving entity: {response.status_code}, {response.text}"

            validate_entity(fetched_entity, new_entity)

    @allure.title("Test get entity")
    @allure.description("Verify that a specific entity can be retrieved")
    @pytest.mark.api
    def test_get_entity(
        self, entity_service: EntityService, new_entity: EntityResponse
    ) -> None:
        """Test that verifies a specific entity can be retrieved."""
        with allure.step(f"Retrieving the created entity with ID {new_entity.id}"):
            response, retrieved_entity = entity_service.get_entity(str(new_entity.id))
            assert (
                response.status_code == 200
            ), f"Error while retrieving entity: {response.status_code}, {response.text}"

        validate_entity(retrieved_entity, new_entity)

    @allure.title("Test get all entities")
    @allure.description("Verify that all entities can be retrieved")
    @pytest.mark.api
    def test_get_all_entities(
        self, entity_service: EntityService, upload_three_entities: list[EntityResponse]
    ) -> None:
        """Test that verifies all entities can be retrieved."""
        with allure.step("Retrieving all entities"):
            response, entities = entity_service.get_all_entities()
            assert response.status_code == 200, (
                f"Error while retrieving entities: {response.status_code}, "
                f"{response.text}"
            )

        with allure.step("Checking that created entities are in the response"):
            retrieved_ids = [entity.id for entity in entities]
            for created_entity in upload_three_entities:
                assert (
                    created_entity.id in retrieved_ids
                ), f"Created entity {created_entity.id} not found in response"

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
    def test_update_entity(
        self, entity_service: EntityService, new_entity: EntityResponse
    ) -> None:
        """Tests that an entity can be updated."""
        updated_entity_request = Payloads.create_entity_request()

        with allure.step(f"Updating entity with ID {new_entity.id}"):
            response = entity_service.api_client.update_entity(
                str(new_entity.id), updated_entity_request.model_dump()
            )
            assert (
                response.status_code == 204
            ), f"Expected status 204, got: {response.status_code}"

        with allure.step("Retrieving the updated entity"):
            response, updated_entity = entity_service.get_entity(str(new_entity.id))
            assert response.status_code == 200, (
                f"Error while retrieving updated entity: "
                f"{response.status_code}, {response.text}"
            )

        validate_entity(updated_entity, updated_entity_request)
        assert (
            updated_entity.id == new_entity.id
        ), f"ID mismatch: expected {new_entity.id}, got {updated_entity.id}"

    @allure.title("Test delete entity")
    @allure.description("Verify that an entity can be deleted successfully")
    @pytest.mark.api
    def test_delete_entity(
        self, entity_service: EntityService, new_entity: EntityResponse
    ) -> None:
        """Tests that an entity can be deleted successfully."""
        with allure.step(f"Deleting the entity with ID {new_entity.id}"):
            delete_response = entity_service.delete_entity(str(new_entity.id))
            assert delete_response.status_code == 204, (
                f"Error while deleting entity: {delete_response.status_code}, "
                f"{delete_response.text}"
            )

        with allure.step(
            f"Attempting to retrieve the deleted entity with ID {new_entity.id}"
        ):
            with pytest.raises(HTTPError) as excinfo:
                entity_service.get_entity(str(new_entity.id))

            assert excinfo.value.response.status_code == 500, (
                f"Expected status 500, but got: "
                f"{excinfo.value.response.status_code}"
            )

        with allure.step(
            "Retrieving all entities and ensuring the deleted entity is not present"
        ):
            all_response, all_entities = entity_service.get_all_entities()
            assert (
                all_response.status_code == 200
            ), f"Error while retrieving all entities: {all_response.status_code}"

            entity_ids = [entity.id for entity in all_entities]
            assert new_entity.id not in entity_ids, (
                f"Deleted entity with ID {new_entity.id} "
                f"is still present among all entities"
            )
