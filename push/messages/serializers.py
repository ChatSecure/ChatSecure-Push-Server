from __future__ import absolute_import
from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200, required=True)
    data = serializers.CharField(allow_null=True, max_length=100, required=False)
    priority = serializers.CharField(allow_null=True, max_length=100, required=False,
                                     help_text="Valid values are 'high' and 'low'. Omitting this key is equivalent to 'low'. Sending 'high' results in a static 'New Message!' notification, low does a background fetch.")
