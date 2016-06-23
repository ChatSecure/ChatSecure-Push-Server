from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from devices.models import APNSDevice, GCMDevice

__author__ = 'dbro'


class APNSRegistrationIdStringField(serializers.Field):
    """
    Strips spaces from strings
    """

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data.replace(" ", "")


class DeviceSerializerMixin(ModelSerializer):

    class Meta:
        # Omit owner because devices are only visible to their owners
        fields = ("name", "id", "active", "registration_id", "device_id", "date_created")
        read_only_fields = ("date_created",)


class APNSDeviceSerializer(ModelSerializer):

    registration_id = APNSRegistrationIdStringField()

    class Meta(DeviceSerializerMixin.Meta):
        model = APNSDevice


class GCMDeviceSerializer(ModelSerializer):

    class Meta(DeviceSerializerMixin.Meta):
        model = GCMDevice
