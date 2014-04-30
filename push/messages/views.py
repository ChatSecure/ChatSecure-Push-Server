from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from messages.serializers import MessageSerializer
from apnsclient import *
from tokens.models import Token
from django.conf import settings
from devices.models import Device

apns_session = Session()


class MessagesViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = MessageSerializer(data=request.DATA)

        if serializer.is_valid():
            token_string = serializer.data['token']
            message_data = serializer.data['data']
            try:
                token = Token.objects.get(token=token_string)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            send_apns(token=token, data=message_data)
            send_gcm(token=token, data=message_data)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def send_apns(token=None, data=None):
    if settings.CHATSECURE_PUSH.get('USE_MESSAGE_QUEUE', False) is True:
        # TODO use Celery instead of blocking here
        print 'Implement Celery!'
    recipient = token.owner
    if not recipient.app.apns_cert or len(recipient.app.apns_cert) == 0:
        return

    apple_devices = recipient.devices.filter(os_type=Device.OS_IOS)

    if len(apple_devices) == 0:
        return

    apns_tokens = []
    for apple_device in apple_devices:
        apns_tokens.append(apple_device.push_token)

    sandbox_mode = recipient.app.sandbox_mode
    push_endpoint = "push_production"
    if sandbox_mode:
        push_endpoint = "push_sandbox"

    connection = apns_session.get_connection(push_endpoint, cert_string=recipient.app.apns_cert)

    # New message to 3 devices. You app will show badge 10 over app's icon.
    message = Message(apns_tokens, alert='Hellloooooo', badge=1)

    # Send the message.
    srv = APNs(connection)
    res = srv.send(message)

    # Check failures. Check codes in APNs reference docs.
    for token, reason in res.failed.items():
        code, errmsg = reason
        print "Device failed: {0}, reason: {1}".format(token, errmsg)

    # Check failures not related to devices.
    for code, errmsg in res.errors:
        print "Error: ", errmsg

    # Check if there are tokens that can be retried
    if res.needs_retry():
        # repeat with retry_message or reschedule your task
        retry_message = res.retry()
        if retry_message:
            print 'Needs a retry!'


def send_gcm(token=None, data=None):
    pass
