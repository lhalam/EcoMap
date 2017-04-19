import random
import string


def generate_random_number(type_of_data, max_value=1000):
    if type_of_data == 'int':
        return str(random.randint(1, max_value))
    elif type_of_data == 'float':
        return str(random.uniform(0.0, max_value))


def generate_random_word(length_of_word=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits)for _ in range(length_of_word))
