from common.serializers import DynamicFieldsModelSerializer
from .models import Team, TeamMember
from users.serializers import UserSerializer


class TeamSerializer(DynamicFieldsModelSerializer):
    leader = UserSerializer()

    class Meta:
        model = Team
        fields = '__all__'


class TeamMemberSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id']
