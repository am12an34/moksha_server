from rest_framework.serializers import ModelSerializer
from .models import Contest, SoloContestRegistration, TeamContestRegistration, TeamContestUserRegistration
from users.serializers import UserSerializer
from common.serializers import DynamicFieldsModelSerializer


class ContestSerializer(ModelSerializer):
    class Meta:
        model = Contest
        exclude = ['is_solo']


class SoloContestRegistrationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SoloContestRegistration
        fields = ['id']


class TeamContestUserRegistrationSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamContestUserRegistration
        fields = ['user']


class TeamContestRegistrationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TeamContestRegistration
        fields = ['id']
