from rest_framework.throttling import UserRateThrottle


class CreateOAuth2TokenRateThrottle(UserRateThrottle):
    scope = "create_oAuth2Token"
