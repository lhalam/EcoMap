import random


def generate_random_number(min_value=1, max_value=1000):
    return str(random.randint(min_value, max_value))

def generate_random_long():
    return str(random.randint(100, 999))