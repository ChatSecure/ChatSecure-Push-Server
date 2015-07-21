from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from messages.serializers import MessageSerializer
from tokens.models import Token
from push_notifications.models import APNSDevice, GCMDevice


class MessagesViewSet(viewsets.ViewSet):
    """
    Messages represent a push message directed at devices belonging to a single [Account](/api/accounts/).

    The `data` parameter must be JSON-compatible.

    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = MessageSerializer

    def create(self, request):
        serializer = MessageSerializer(data=request.DATA)

        if serializer.is_valid():
            token_string = serializer.data['token']
            message_data = serializer.data.get('data')
            try:
                token = Token.objects.get(token=token_string)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            send_message(token=token, data=message_data)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_message(token=None, data=None, broadcast=True):
    '''

    Send a push message containing to the owner of the provided token.
    data is packaged within a 'message' dictionary as below:

    { ... APNS / GCM Payload
        'message' : {
            'token' : 'recipient_whitelist_token',
            'data' : 'data'
        }
    }

    See "APNS Documentation":https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html
    See "GCM Documentation":https://developers.google.com/cloud-messaging/server-ref#downstream

    :param token: the whitelist token corresponding to the specific device to push, if broadcast is False
    :param data: APNS currently supports 2kb and GCM 4kb
    :param broadcast: whether to alert all devices belonging to recipient (default True)
    '''

    message = {
        'message': {
            'data': data,
            'token': token.token
        }
    }

    recipient = token.owner
    if broadcast is True:
        apns_devices = APNSDevice.objects.filter(user__pk=recipient.pk)
        gcm_devices = GCMDevice.objects.filter(user__pk=recipient.pk)
        apns_devices.send_message(message=None, extra=message, content_available=True)
        gcm_devices.send_message(message)
    else:
        apns_device = token.apns_device
        gcm_device = token.gcm_device

        if apns_device:
            apns_device.send_message(message=None, extra=message, content_available=True)
        elif gcm_device:
            gcm_device.send_message(message)
