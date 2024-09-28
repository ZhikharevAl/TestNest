import allure
import pytest
from pydantic import ValidationError

from services.entity.models.entity_model import EntityRequest, EntityResponse


def validate_entity(
    entity: EntityResponse | dict,
    expected_entity: EntityRequest | EntityResponse | dict = None,
) -> EntityResponse:
    """
    Validates the entity and compares it with the expected entity if provided.

    :param entity: The entity to validate (EntityResponse or dict)
    :param expected_entity: The expected entity to
    compare against (EntityRequest, EntityResponse, or dict, optional)
    """
    with allure.step("Entity validation"):
        try:
            if isinstance(entity, dict):
                validated_entity = EntityResponse.model_validate(entity)
            else:
                validated_entity = entity
        except ValidationError as e:
            pytest.fail(f"Entity validation failed: {e}")

    if expected_entity:
        if isinstance(expected_entity, dict):
            expected_entity = EntityRequest.model_validate(expected_entity)

        with allure.step("Checking entity title correctness"):
            assert validated_entity.title == expected_entity.title, (
                f"Title mismatch: expected {expected_entity.title}, "
                f"got {validated_entity.title}"
            )

        with allure.step("Checking 'verified' field"):
            assert (
                validated_entity.verified == expected_entity.verified
            ), f"Expected {expected_entity.verified}, got {validated_entity.verified}"

        with allure.step("Checking 'important_numbers' field"):
            assert (
                validated_entity.important_numbers == expected_entity.important_numbers
            ), (
                f"Expected {expected_entity.important_numbers}, "
                f"got {validated_entity.important_numbers}"
            )

        with allure.step("Checking additional data"):
            assert (
                validated_entity.addition.additional_info
                == expected_entity.addition.additional_info
            ), (
                f"Expected additional_info='"
                f"{expected_entity.addition.additional_info}', "
                f"got '{validated_entity.addition.additional_info}'"
            )

            assert (
                validated_entity.addition.additional_number
                == expected_entity.addition.additional_number
            ), (
                f"Expected additional_number='"
                f"{expected_entity.addition.additional_number}', "
                f"got '{validated_entity.addition.additional_number}'"
            )

        if hasattr(expected_entity, "id"):
            with allure.step("Checking entity ID correctness"):
                assert validated_entity.id == expected_entity.id, (
                    f"ID mismatch: expected {expected_entity.id}, "
                    f"got {validated_entity.id}"
                )

    return validated_entity
