from rest_framework import serializers
from push_notifications.models import APNSDevice, GCMDevice
from tokens.models import Token


class TokenSerializer(serializers.HyperlinkedModelSerializer):

    apns_device = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=APNSDevice.objects.all())
    gcm_device = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=GCMDevice.objects.all())

    class Meta:
        model = Token
        fields = ('id', 'url', 'name', 'token', 'apns_device', 'gcm_device')
        read_only_fields = ('token',)

    def __init__(self, *args, **kwargs):
        super(TokenSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request', None):
            # Restrict the queryset of APNS and GCM devices to those owned by the request's user
            apns_device = self.fields.get('apns_device')
            apns_device.queryset = apns_device.queryset.filter(user=self.context['request'].user)

            gcm_device = self.fields.get('gcm_device')
            gcm_device.queryset = gcm_device.queryset.filter(user=self.context['request'].user)

    def validate(self, data):
        """
        Check that an APNS or a GCM device was specified
        """
        if not data.get('apns_device', None) and not data.get('gcm_device', None):
            raise serializers.ValidationError("Either an APNS or GCM device must be specified")

        if data.get('apns_device', None) and data.get('gcm_device', None):
            raise serializers.ValidationError("Only one APNS or one GCM device may be specified")

        return data
