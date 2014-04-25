from rest_framework import serializers
from tokens.models import Token


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'url', 'name', 'token',)
        read_only_fields = ('token',)
