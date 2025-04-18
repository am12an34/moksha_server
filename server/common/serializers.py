from rest_framework.serializers import ModelSerializer


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        empty = kwargs.pop('empty', False)

        super().__init__(*args, **kwargs)

        if empty:
            self.fields.clear()

        if fields is not None:
            for related_name in fields:
                self.fields[related_name] = fields[related_name]
