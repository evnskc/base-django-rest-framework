from rest_framework.throttling import UserRateThrottle


class CreateUserRateThrottle(UserRateThrottle):
    scope = "create_user"


class EmailUserRateThrottle(UserRateThrottle):
    scope = "email_user"
