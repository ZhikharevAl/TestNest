from data.customer import Customer


def create_customers(num_customers: int) -> list:
    """
    Create a list of customers.

    This function generates a specified number of Customer objects
    and returns them in a list.

    Args:
        num_customers (int): The number of customers to create.

    Returns:
        list: A list of Customer objects.
    """
    return [Customer() for _ in range(num_customers)]
