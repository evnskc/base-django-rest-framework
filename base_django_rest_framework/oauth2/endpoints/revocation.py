from authlib.integrations.django_oauth2 import RevocationEndpoint as _RevocationEndpoint


class RevocationEndpoint(_RevocationEndpoint):
    CLIENT_AUTH_METHODS = ["none"]
