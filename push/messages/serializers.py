from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    whitelist_token = serializers.CharField(max_length=200, required=True)
    data = serializers.CharField(max_length=100, required=False)
