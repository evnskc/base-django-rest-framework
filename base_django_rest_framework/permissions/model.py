from rest_framework.permissions import DjangoModelPermissions


class ModelPermissions(DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map.update({"GET": ['%(app_label)s.view_%(model_name)s']})

    def has_permission(self, request, view):
        return super().has_permission(request, view) and bool(request.user and request.user.is_verified)
