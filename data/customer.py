from dataclasses import dataclass, field

from data.providers import fake


@dataclass(slots=True)
class Customer:
    post_code: str = field(default_factory=lambda: fake.custom_postcode())
    first_name: str = field(init=False)
    last_name: str = field(default_factory=lambda: fake.last_name())

    def __post_init__(self):
        self.first_name = fake.custom_first_name(self.post_code)
