from rest_framework import serializers
from accounts.models import PushUser


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, allow_null=True, required=False)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=100, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushUser
        fields = ('username', 'email', 'id')
        read_only_fields = ('username',)