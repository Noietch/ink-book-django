import random
import string


def get_verification_code():
    length_of_string = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
