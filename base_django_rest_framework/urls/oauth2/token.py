from base_django_rest_framework.routers import Router
from base_django_rest_framework.views import OAuth2TokenViewSet

app_name = "tokens"

router = Router()
router.register("", OAuth2TokenViewSet, basename="oAuth2Token")

urlpatterns = router.urls
