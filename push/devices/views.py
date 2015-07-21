from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet

class _APNSDeviceAuthorizedViewSet(APNSDeviceAuthorizedViewSet):
    """
    An [APNS](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html) compatible device.

    ## Registration ID (Required)

    The APNS Device Token, presented as a 64 character string.

    ## Device ID (Optional)

    Currently unused. Any unique identifier you'd like to use to identify this device.

    ## Next Steps

    After creating a device you'll typically want to create a [Token](/api/tokens) to allow others to send it push messages.

    """

class _GCMDeviceAuthorizedViewSet(GCMDeviceAuthorizedViewSet):
    """
    A [GCM](https://developers.google.com/cloud-messaging/server-ref#downstream) compatible device.

    ## Registration ID (Required)

    Your registration ID is the [`GoogleCloudMessaging.INSTANCE_ID_SCOPE`](https://github.com/googlesamples/google-services/blob/e06754fc7d0e4bf856c001a82fb630abd1b9492a/android/gcm/app/src/main/java/gcm/play/android/samples/com/gcmquickstart/RegistrationIntentService.java#L54) token.

    When this identifier changes you should use this API to update your device.

    ## Device ID (Optional)

    Currently unused. Any unique identifier you'd like to use to identify this device as its Registraion ID changes.
    Android does not provide a universal device identifier, but there are [reasonable solutions](http://stackoverflow.com/questions/2785485/is-there-a-unique-android-device-id/2853253#2853253)

    ## Next Steps

    After creating a device you'll typically want to create a [Token](/api/tokens) to allow others to send it push messages.

    """

