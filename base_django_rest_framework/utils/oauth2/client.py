from django.utils.crypto import get_random_string


def client_id_generator():
    return get_random_string(48)
