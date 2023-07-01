from base_django_rest_framework.routers import Router

from base_django_rest_framework.views import UserViewSet

app_name = "users"

router = Router()
router.register("", UserViewSet, basename="user")

urlpatterns = router.urls
