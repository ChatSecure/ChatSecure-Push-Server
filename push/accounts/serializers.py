from rest_framework import serializers
from accounts.models import PushUser


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=False)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=100)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushUser
        fields = ('username', 'email')
        read_only_fields = ('username',)