from __future__ import absolute_import
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import ReadOnlyField

from rest_framework.relations import PrimaryKeyRelatedField
from api.serializers import NonNullSerializer
from devices.models import APNSDevice, GCMDevice
from tokens.models import Token


class TokenSerializer(NonNullSerializer, serializers.ModelSerializer):

    apns_device = PrimaryKeyRelatedField(allow_null=True, required=False, queryset=APNSDevice.objects.all())
    gcm_device = PrimaryKeyRelatedField(allow_null=True, required=False, queryset=GCMDevice.objects.all())
    date_expires = ReadOnlyField(source="get_expiry_date")

    class Meta:
        model = Token
        fields = ('name', 'token', 'apns_device', 'gcm_device', 'date_expires')
        read_only_fields = ('token', 'date_expires')

    def __init__(self, *args, **kwargs):
        super(TokenSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        # If we have an authenticated user, only reveal devices they own
        if request is not None and request.user is not None and not isinstance(request.user, AnonymousUser):
            # Restrict the queryset of APNS and GCM devices to those owned by the request's user
            apns_device = self.fields.get('apns_device')
            apns_device.queryset = apns_device.queryset.filter(owner=request.user)

            gcm_device = self.fields.get('gcm_device')
            gcm_device.queryset = gcm_device.queryset.filter(owner=request.user)

        else:
            raise PermissionDenied

    def validate(self, data):
        """
        Check that an APNS or a GCM device was specified
        """
        if not data.get('apns_device', None) and not data.get('gcm_device', None):
            raise serializers.ValidationError("Either an APNS or GCM device must be specified")

        if data.get('apns_device', None) and data.get('gcm_device', None):
            raise serializers.ValidationError("Only one APNS or one GCM device may be specified")

        return data
