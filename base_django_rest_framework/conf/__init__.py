from base_django_rest_framework.utils import token_generator

AUTH_USER_MODEL = "base_django_rest_framework.User"

INCLUDE_USERNAME_COLUMN = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "base_django_rest_framework.authentication.OAuth2Authentication"
    ],

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],

    "DEFAULT_THROTTLE_RATES": {
        "user": "60/minute",
        "anon": "60/minute",
        "create_oAuth2Token": "12/hour",
        "create_user": "12/hour",
        "email_user": "12/hour"
    },

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 25,

    "TEST_REQUEST_DEFAULT_FORMAT": "json"
}

AUTHLIB_OAUTH2_PROVIDER = {
    "access_token_generator": token_generator,
    "refresh_token_generator": token_generator
}

EMAIL_CONFIRMATION_URL = "https://example.com/email/verify/?signature={signature}"
EMAIL_CHANGE_URL = "https://example.com/email/update/?signature={signature}"
PASSWORD_RESET_URL = "https://example.com/password/reset/?signature={signature}"
