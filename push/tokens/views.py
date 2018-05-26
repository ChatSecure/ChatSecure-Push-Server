from __future__ import absolute_import
from rest_framework import viewsets
from rest_framework import permissions
from tokens.models import Token
from tokens.serializers import TokenSerializer
import binascii
import os
from api.permissions import OwnerOnlyPermission


class TokenViewSet(viewsets.ModelViewSet):
    """
    Tokens represent revokable authorization to send push messages to ** all of the owner's devices**. It's reccommended
    an owner request a new token for each sender, so that he/she may revoke push access per-sender. Tokens have a
    time-to-live, so take note of the **date_expires** attribute.

    A token is created with reference to **one** of its owner's devices, but it grants the bearer authorization to push
    to that device or **all of the owner's devices**.

    ## Next Steps

    After creating a token you'll typically share it with **one** sender who you wish to receive push messages from.

    After receiving another's token, you'll typically send them a [Message](/api/v1/messages/).

    """

    serializer_class = TokenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOnlyPermission)
    lookup_field = "token"

    def get_queryset(self):
        """
        This view should return a list of all the devices
        for the currently authenticated user.
        """
        user = self.request.user
        if not user.is_authenticated:
            return []
        return Token.objects.filter(owner=user)

    def perform_create(self, serializer):

        # TODO : We should catch the event where the resulting token violates unique column constraint
        raw_token = binascii.hexlify(os.urandom(20))
        token = str(raw_token, 'ascii')
        serializer.save(owner=self.request.user, token=token)
