from django.contrib.auth.models import Group
from rest_framework import serializers
from accounts.models import PushUser


class PushUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PushUser
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')