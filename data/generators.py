from data.customer import Customer


def create_customers(num_customers):
    return [Customer() for _ in range(num_customers)]
