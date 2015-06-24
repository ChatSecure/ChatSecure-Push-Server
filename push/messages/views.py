from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from messages.serializers import MessageSerializer
from tokens.models import Token
from push_notifications.models import APNSDevice, GCMDevice


class MessagesViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = MessageSerializer

    def create(self, request):
        serializer = MessageSerializer(data=request.DATA)

        if serializer.is_valid():
            token_string = serializer.data['token']
            message_data = serializer.data['data']
            try:
                token = Token.objects.get(token=token_string)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            send_message(token=token, data=message_data)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_message(token=None, data=None, broadcast=True):
    recipient = token.owner
    if broadcast is True:
        apns_devices = APNSDevice.objects.filter(user__pk=recipient.pk)
        gcm_devices = GCMDevice.objects.filter(user__pk=recipient.pk)
        apns_devices.send_message("Hello Broadcast")
        gcm_devices.send_message("Hello Broadcast")
    else:
        apns_device = token.apns_device
        gcm_device = token.gcm_device

        if apns_device:
            apns_device.send_message("Hello")
        elif gcm_device:
            gcm_device.send_message("Hello")
