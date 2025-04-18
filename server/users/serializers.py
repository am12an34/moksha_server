from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from common.serializers import DynamicFieldsModelSerializer
from .models import Profile


class ProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Profile
        fields = ['tag', 'phone_no', 'institution', 'avatar_idx']


class AuthUserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'profile'
        ]

    def to_representation(self, obj):
        # Move all fields from profile to user representation.
        representation = super().to_representation(obj)
        profile_representation = representation.pop('profile')

        for key in profile_representation:
            representation[key] = profile_representation[key]

        return representation


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']

    def to_representation(self, obj):
        # Move 'avatar_idx' from profile to user representation.
        representation = super().to_representation(obj)
        profile_representation = representation.pop('profile')
        representation['avatar_idx'] = profile_representation['avatar_idx']
        return representation
