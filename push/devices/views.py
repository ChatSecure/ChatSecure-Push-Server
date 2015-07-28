from rest_framework.viewsets import ModelViewSet
from api.permissions import OwnerOnlyPermission
from devices.models import APNSDevice, GCMDevice
from devices.serializers import APNSDeviceSerializer, GCMDeviceSerializer


class DeviceViewSetMixin(object):
    lookup_field = "id"

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(owner=self.request.user)


class APNSDeviceAuthorizedViewSet(OwnerOnlyPermission, DeviceViewSetMixin, ModelViewSet):
    """
    A [GCM](https://developers.google.com/cloud-messaging/server-ref#downstream) compatible device.

    ## Registration ID (Required)

    Your registration ID is the [`GoogleCloudMessaging.INSTANCE_ID_SCOPE`](https://github.com/googlesamples/google-services/blob/e06754fc7d0e4bf856c001a82fb630abd1b9492a/android/gcm/app/src/main/java/gcm/play/android/samples/com/gcmquickstart/RegistrationIntentService.java#L54) token.

    When this identifier changes you should use this API to update your device.

    ## Device ID (Optional)

    Currently unused. Any unique identifier you'd like to use to identify this device as its Registraion ID changes.
    Android does not provide a universal device identifier, but there are [reasonable solutions](http://stackoverflow.com/questions/2785485/is-there-a-unique-android-device-id/2853253#2853253)

    ## Next Steps

    After creating a device you'll typically want to create a [Token](/api/v1/tokens) to allow others to send it push messages.

    """

    queryset = APNSDevice.objects.all()
    serializer_class = APNSDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class GCMDeviceAuthorizedViewSet(OwnerOnlyPermission, DeviceViewSetMixin, ModelViewSet):
    """
    An [APNS](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html) compatible device.

    ## Registration ID (Required)

    The APNS Device Token, presented as a 64 character string.

    ## Device ID (Optional)

    Currently unused. Any unique identifier you'd like to use to identify this device.

    ## Next Steps

    After creating a device you'll typically want to create a [Token](/api/v1/tokens) to allow others to send it push messages.

    """

    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
