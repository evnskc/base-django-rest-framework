from django.contrib.auth import get_user_model
from django.core.signing import dumps, loads, BadSignature


class UserSigner:
    @staticmethod
    def sign(data):
        return dumps(data)

    @staticmethod
    def unsign(signature, max_age):
        data = loads(signature, max_age=max_age)
        try:
            return get_user_model().objects.get(**data["user"]), data.get("extra", {})
        except get_user_model().DoesNotExist:
            raise BadSignature()
