import random
import string

MIN_LENGTH = 6


def generate_random_string(length=6):
    return ''.join((random.choice(string.ascii_lowercase) for x in range(length)))

