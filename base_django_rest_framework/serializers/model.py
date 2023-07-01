from rest_framework.serializers import ModelSerializer as _ModelSerializer


class ModelSerializer(_ModelSerializer):

    def __init__(self, *args, fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field in existing - allowed:
                self.fields.pop(field)
