import logging

import pytest

from config.config_api.config import BASE_URL
from services.entity.api_client import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Fixture to create and return an APIClient instance."""
    return APIClient(BASE_URL)


@pytest.fixture
def entity_id(api_client: APIClient) -> str:
    """Fixture to create and yield a new entity ID."""
    entity_id = api_client.create_entity().text
    yield entity_id
    api_client.delete_entity(entity_id)


def pytest_configure() -> None:
    """Log configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("faker").setLevel(logging.WARNING)
