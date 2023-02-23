from . import models
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'password')


class VerifyUserEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


