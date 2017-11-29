import random
import string


def get_random_string(length=32, allowed_characters=None):
    if not allowed_characters:
        allowed_characters = string.letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join([random.SystemRandom().choice(allowed_characters) for _ in range(length)])
