from faker import Faker
from faker.providers import BaseProvider
import random
import string


class CustomProvider(BaseProvider):
    @staticmethod
    def custom_postcode():
        return "".join(random.choices(string.digits, k=10))

    @staticmethod
    def custom_first_name(postcode):
        def digit_to_letter(digit):
            return chr((int(digit) % 26) + 97)

        name = ""
        for i in range(0, 10, 2):
            two_digit = int(postcode[i : i + 2])
            name += digit_to_letter(two_digit)
        return name.capitalize()


fake = Faker()
fake.add_provider(CustomProvider)
