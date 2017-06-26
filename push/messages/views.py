from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from devices.models import APNSDevice, GCMDevice
from messages.messenger import send_gcm, send_apns
from messages.serializers import MessageSerializer
from tokens.models import Token


class MessagesViewSet(viewsets.ViewSet):
    """
    Messages represent a push message directed at devices belonging to a single [Account](/api/v1/accounts/).

    The `data` parameter must be JSON-compatible, as it is delivered to the client in a JSON dictionary:

        { ... APNS / GCM Payload
            'message' : {
                'token' : '<token>',
                'data' : '<data>'
            }
        }

    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = MessageSerializer

    def create(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            token_string = serializer.data['token']
            message_data = serializer.data.get('data', None)
            alert_type = serializer.data.get('type', 'silent')  # Default to silent
            try:
                token = Token.objects.get(token=token_string)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            send_message(token=token, data=message_data, alert_type=alert_type)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_message(token=None, data=None, broadcast=True, alert_type=None):
    '''

    Send a push message containing to the owner of the provided token.
    data is packaged within a 'message' dictionary as below:

    { ... APNS / GCM Payload
        'message' : {
            'token' : 'recipient_whitelist_token',
            'data' : 'data',
            'type' : 'message'
        }
    }

    See "APNS Documentation":https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html
    See "GCM Documentation":https://developers.google.com/cloud-messaging/server-ref#downstream

    :param token: the whitelist token corresponding to the specific device to push, if broadcast is False
    :param data: APNS currently supports 2kb and GCM 4kb
    :param broadcast: whether to alert all devices belonging to recipient (default True)
    :param alert_type: Valid values are 'typing' and 'message' and 'silent'. Omitting this key is equivalent to 'silent'
    '''

    message = {
        'message': {
            'data': data,
            'token': token.token
        }
    }

    recipient = token.owner
    if broadcast is True:
        apns_devices = APNSDevice.objects.filter(owner__pk=recipient.pk)
        gcm_devices = GCMDevice.objects.filter(owner__pk=recipient.pk)

        if apns_devices.count() > 0:
            apns_registration_ids = [device.registration_id for device in apns_devices]
            send_apns(registration_ids=apns_registration_ids, message=message, alert_type=alert_type, content_available=True)

        if gcm_devices.count() > 0:
            gcm_registration_ids = [device.registration_id for device in gcm_devices]
            send_gcm(registration_ids=gcm_registration_ids, message=message)
    else:
        apns_device = token.apns_device
        gcm_device = token.gcm_device

        if apns_device:
            send_apns(registration_ids=apns_device.registration_id, message=message, alert_type=alert_type, content_available=True)
        elif gcm_device:
            send_gcm(registration_ids=gcm_device.registration_id, message=message)
