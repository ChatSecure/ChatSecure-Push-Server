from rest_framework import serializers
from tokens.models import WhitelistToken


class WhitelistTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhitelistToken
        fields = ('id', 'name', 'token',)
        read_only_fields = ('token',)
