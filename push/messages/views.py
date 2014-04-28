from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from messages.serializers import MessageSerializer
from apnsclient import *
from tokens.models import Token

session = Session()


class MessagesViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    permission_classes = (permissions.AllowAny,)


    def create(self, request):

        # return Response({u'success': True})

        serializer = MessageSerializer(data=request.DATA)

        if serializer.is_valid():
            token_string = serializer.data.get('whitelist_token', None)
            token = Token.objects.get(token=token_string)
            recipient = token.owner

            apns_tokens = []

            for device in recipient.devices.all():
                apns_tokens.append(device.push_token)

            con = session.get_connection("push_sandbox", cert_string=recipient.app.apns_dev)

            # New message to 3 devices. You app will show badge 10 over app's icon.
            message = Message(apns_tokens, alert='Hellloooooo', badge=1)

            # Send the message.
            srv = APNs(con)
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

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
