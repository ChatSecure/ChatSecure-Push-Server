from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200, required=True)
    data = serializers.CharField(allow_null=True, max_length=100, required=False)
