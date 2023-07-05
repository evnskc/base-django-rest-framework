from authlib.common.security import generate_token


def token_generator(*args, **kwargs):
    return generate_token(48)
