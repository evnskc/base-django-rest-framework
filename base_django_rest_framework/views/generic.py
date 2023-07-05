from rest_framework.viewsets import GenericViewSet as _GenericViewSet


class GenericViewSet(_GenericViewSet):
    lookup_url_converter = None
    field_map = {}

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, fields=self.field_map.get(self.action), **kwargs)
