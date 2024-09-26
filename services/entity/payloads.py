from typing import Any

from faker import Faker

from services.entity.models.entity_model import AdditionRequest, EntityRequest

fake = Faker()


class Payloads:
    """A class used to represent Payloads."""

    @staticmethod
    def generate_entity_payload() -> dict[str, Any]:
        """Generate a dictionary representing an entity payload."""
        return {
            "title": fake.sentence(nb_words=2),
            "verified": fake.boolean(),
            "important_numbers": [fake.random_int(min=1, max=100) for _ in range(3)],
            "addition": {
                "additional_info": fake.sentence(nb_words=3),
                "additional_number": fake.random_int(min=1, max=1000),
            },
        }

    @classmethod
    def create_entity_request(
        cls, payload: dict[str, Any] | None = None
    ) -> EntityRequest:
        """Create an EntityRequest object from a payload."""
        if payload is None:
            payload = cls.generate_entity_payload()

        if "addition" not in payload or payload["addition"] is None:
            payload["addition"] = {
                "additional_info": fake.sentence(nb_words=3),
                "additional_number": fake.random_int(min=1, max=1000),
            }

        return EntityRequest(
            title=payload["title"],
            verified=payload["verified"],
            important_numbers=payload["important_numbers"],
            addition=AdditionRequest(**payload["addition"]),
        )
