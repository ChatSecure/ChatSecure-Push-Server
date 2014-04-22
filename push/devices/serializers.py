from rest_framework import serializers
from devices.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('os_type', 'os_version', 'device_name', 'push_token')
        read_only_fields = ('owner',)
