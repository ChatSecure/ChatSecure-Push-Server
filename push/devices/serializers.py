from rest_framework.serializers import ModelSerializer
from devices.models import APNSDevice, GCMDevice

__author__ = 'dbro'


class DeviceSerializerMixin(ModelSerializer):

    class Meta:
        # Omit owner because devices are only visible to their owners
        fields = ("name", "id", "active", "registration_id", "device_id", "date_created", "xmpp_push_service")
        read_only_fields = ("date_created",)


class APNSDeviceSerializer(ModelSerializer):

    class Meta(DeviceSerializerMixin.Meta):
        model = APNSDevice


class GCMDeviceSerializer(ModelSerializer):

    class Meta(DeviceSerializerMixin.Meta):
        model = GCMDevice
