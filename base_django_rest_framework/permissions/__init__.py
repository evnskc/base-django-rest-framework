from .model import ModelPermissions
from .user import IsSuperuser, IsSelf, IsOwner


class IsSelfOrHasModelPermissions(IsSelf):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) or ModelPermissions().has_permission(request, view)


class IsNotSelfAndIsSuperuser(IsSelf):
    def has_object_permission(self, request, view, obj):
        return not super().has_object_permission(request, view, obj) and IsSuperuser().has_permission(request, view)


class IsNotSelfAndHasModelPermissions(IsSelf):
    def has_object_permission(self, request, view, obj):
        return not super().has_object_permission(request, view, obj) and ModelPermissions().has_permission(request,
                                                                                                           view)


class IsOwnerOrHasModelPermissions(IsOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) or ModelPermissions().has_permission(request, view)
