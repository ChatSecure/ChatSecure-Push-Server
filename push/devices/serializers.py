from rest_framework import serializers
from devices.models import Device


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'url', 'os_type', 'os_version', 'device_name', 'push_token')
