import logging

import pytest

from config.config_api.config import BASE_URL
from services.entity.api_client import APIClient
from services.entity.entity_service import EntityService
from services.entity.models.entity_model import EntityResponse


@pytest.fixture
def api_client() -> APIClient:
    """Fixture to create and return an APIClient instance."""
    return APIClient(BASE_URL)


@pytest.fixture
def entity_service(api_client: APIClient) -> EntityService:
    """Fixture for creating an EntityService instance."""
    return EntityService(api_client)


@pytest.fixture
def new_entity(entity_service: EntityService) -> EntityResponse:
    """Fixture to create a new entity, return its data, deleting it after the test."""
    _, entity = entity_service.create_entity()
    yield entity
    try:
        entity_service.delete_entity(str(entity.id))
    except Exception as e:
        error_message = f"Failed to delete entity {entity.id}: {e!s}"
        logging.exception(error_message)


@pytest.fixture
def upload_three_entities(entity_service: EntityService) -> list[EntityResponse]:
    """Fixture to create 3 new entities, return data, deleting them after the test."""
    entities = []
    for _ in range(3):
        _, entity = entity_service.create_entity()
        entities.append(entity)
    yield entities
    for entity in entities:
        try:
            entity_service.delete_entity(str(entity.id))
        except Exception as e:
            error_message = f"Failed to delete entity {entity.id}: {e!s}"
            logging.exception(error_message)


def pytest_configure() -> None:
    """Log configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("faker").setLevel(logging.WARNING)
