from rest_framework.mixins import (ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin)

from .generic import GenericViewSet


class ModelViewSet(ListModelMixin,
                   CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    pass


class ReadOnlyModelViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass
