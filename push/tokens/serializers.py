from rest_framework import serializers
from tokens.models import WhitelistToken


class WhitelistTokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WhitelistToken
        fields = ('id', 'url', 'name', 'token',)
        read_only_fields = ('token',)
