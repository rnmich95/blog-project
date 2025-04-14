import random
import string


def random_string(n:int=4) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))