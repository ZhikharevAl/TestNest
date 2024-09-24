from typing import ClassVar

from faker import Faker

fake = Faker()

class Payloads:
    """Class for generating payloads with fake data."""


    create_entity: ClassVar[dict] = {
        "addition": {
            "additional_info": fake.sentence(nb_words=3),
            "additional_number": fake.random_int(min=1, max=1000),
        },
        "important_numbers": [fake.random_int(min=1, max=100) for _ in range(3)],
        "title": fake.sentence(nb_words=2),
        "verified": fake.boolean(),
    }
