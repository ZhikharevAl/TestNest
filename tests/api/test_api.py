import allure
import pytest
from requests import HTTPError

from services.entity.entity_service import EntityService
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
    def test_create_entity(
        self, entity_service: EntityService, create_entity: EntityResponse
    ) -> None:
        """Test create entity."""
        created_entity = create_entity

        with allure.step(f"Verifying the created entity with ID {created_entity.id}"):
            assert isinstance(
                created_entity.id, int
            ), f"Expected a numeric ID, got: {created_entity.id}"

            response, fetched_entity = entity_service.get_entity(str(created_entity.id))
            assert (
                response.status_code == 200
            ), f"Error while retrieving entity: {response.status_code}, {response.text}"

            validate_entity(fetched_entity, created_entity)

    @allure.title("Test get entity")
    @allure.description("Verify that a specific entity can be retrieved")
    @pytest.mark.api
    def test_get_entity(
        self, entity_service: EntityService, create_entity: EntityResponse
    ) -> None:
        """Test that verifies a specific entity can be retrieved."""
        created_entity = create_entity

        with allure.step(f"Retrieving the created entity with ID {created_entity.id}"):
            response, retrieved_entity = entity_service.get_entity(
                str(created_entity.id)
            )
            assert (
                response.status_code == 200
            ), f"Error while retrieving entity: {response.status_code}, {response.text}"

        validate_entity(retrieved_entity, created_entity)

    @allure.title("Test get all entities")
    @allure.description("Verify that all entities can be retrieved")
    @pytest.mark.api
    def test_get_all_entities(self, entity_service: EntityService) -> None:
        """Test that verifies all entities can be retrieved."""
        created_entities = []
        for _ in range(3):
            with allure.step("Creating a new entity"):
                _, entity = entity_service.create_entity()
                created_entities.append(entity)

        try:
            with allure.step("Retrieving all entities"):
                response, entities = entity_service.get_all_entities()
                assert response.status_code == 200, (
                    f"Error while retrieving entities: {response.status_code}, "
                    f"{response.text}"
                )

            with allure.step("Checking that created entities are in the response"):
                retrieved_ids = [entity.id for entity in entities]
                for created_entity in created_entities:
                    assert (
                        created_entity.id in retrieved_ids
                    ), f"Created entity {created_entity.id} not found in response"

            with allure.step("Checking the types of the retrieved objects"):
                assert all(
                    isinstance(entity, EntityResponse) for entity in entities
                ), "Not all elements are EntityResponse objects"

            for entity in entities:
                validate_entity(entity)

        finally:
            for entity in created_entities:
                with allure.step(f"Deleting test entity {entity.id}"):
                    entity_service.delete_entity(str(entity.id))

    @allure.title("Test update entity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that an entity can be updated successfully")
    @pytest.mark.api
    def test_update_entity(
        self, entity_service: EntityService, create_entity: EntityResponse
    ) -> None:
        """Tests that an entity can be updated."""
        created_entity = create_entity

        updated_entity_request = Payloads.create_entity_request()

        with allure.step(f"Updating entity with ID {created_entity.id}"):
            response, _ = entity_service.update_entity(
                str(created_entity.id), updated_entity_request
            )
            assert (
                response.status_code == 204
            ), f"Expected status 204, got: {response.status_code}"

        with allure.step("Retrieving the updated entity"):
            response, updated_entity = entity_service.get_entity(str(created_entity.id))
            assert response.status_code == 200, (
                f"Error while retrieving updated entity: "
                f"{response.status_code}, {response.text}"
            )

        validate_entity(updated_entity, updated_entity_request)
        assert (
            updated_entity.id == created_entity.id
        ), f"ID mismatch: expected {created_entity.id}, got {updated_entity.id}"

    @allure.title("Test delete entity")
    @allure.description("Verify that an entity can be deleted successfully")
    @pytest.mark.api
    def test_delete_entity(
        self, entity_service: EntityService, create_and_delete_entity: EntityResponse
    ) -> None:
        """Tests that an entity can be deleted successfully."""
        created_entity = create_and_delete_entity

        with allure.step(f"Deleting the entity with ID {created_entity.id}"):
            delete_response = entity_service.delete_entity(str(created_entity.id))
            assert delete_response.status_code == 204, (
                f"Error while deleting entity: {delete_response.status_code}, "
                f"{delete_response.text}"
            )

        with allure.step(
            f"Attempting to retrieve the deleted entity with ID {created_entity.id}"
        ):
            with pytest.raises(HTTPError) as excinfo:
                entity_service.get_entity(str(created_entity.id))

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
            assert created_entity.id not in entity_ids, (
                f"Deleted entity with ID {created_entity.id} "
                f"is still present among all entities"
            )
