from dataclasses import dataclass, field

from data.providers import fake


@dataclass(slots=True)
class Customer:
    """
    A class representing a customer.

    This dataclass contains information about a customer, including
    their postcode, first name, and last name. The first name is
    generated based on the postcode after initialization.

    Attributes:
        post_code (str): The postcode of the customer.
        first_name (str): The first name of the customer, generated from the postcode.
        last_name (str): The last name of the customer.
    """

    post_code: str = field(default_factory=lambda: fake.custom_postcode())
    first_name: str = field(init=False)
    last_name: str = field(default_factory=lambda: fake.last_name())

    def __post_init__(self) -> None:
        """
        Post-initialization processing.

        This method is called automatically after the dataclass
        is initialized. It sets the first name of the customer
        based on the custom first name generated from the postcode.
        """
        self.first_name = fake.custom_first_name(self.post_code)
