import secrets
import string

from faker import Faker
from faker.providers import BaseProvider


class CustomProvider(BaseProvider):
    """
    A custom provider for generating custom postcodes and first names.

    This class contains static methods for generating custom postcodes
    consisting of 10 random digits and custom first names based on a given postcode.
    """

    @staticmethod
    def custom_postcode() -> str:
        """
        Generate a custom postcode consisting of 10 random digits.

        Returns:
            str: The generated custom postcode.
        """
        return "".join(secrets.choice(string.digits) for _ in range(10))

    @staticmethod
    def custom_first_name(postcode: str) -> str:
        """
        Generate a custom first name based on the given postcode.

        This method converts each digit of the postcode to a corresponding letter
        and concatenates them to form a custom first name.

        Args:
            postcode (str): The postcode to convert.

        Returns:
            str: The generated custom first name.
        """

        def digit_to_letter(digit: int) -> str:
            return chr((int(digit) % 26) + 97)

        name = ""
        for i in range(0, 10, 2):
            two_digit = int(postcode[i : i + 2])
            name += digit_to_letter(two_digit)
        return name.capitalize()


fake = Faker()
fake.add_provider(CustomProvider)
