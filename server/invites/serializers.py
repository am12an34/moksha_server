from common.serializers import DynamicFieldsModelSerializer
from .models import Invite


class InviteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Invite
        fields = ['id']
