from base_django_rest_framework.routers import Router
from base_django_rest_framework.views import OAuth2ClientViewSet

app_name = "clients"

router = Router()
router.register("", OAuth2ClientViewSet, basename="oAuth2Client")

urlpatterns = router.urls
