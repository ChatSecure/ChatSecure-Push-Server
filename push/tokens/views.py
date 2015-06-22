from rest_framework import viewsets
from rest_framework import permissions
from tokens.models import Token
from tokens.serializers import TokenSerializer
import binascii
import os
from api.permissions import OwnerOnlyPermission


class TokenViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = TokenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOnlyPermission)

    def get_queryset(self):
        """
        This view should return a list of all the devices
        for the currently authenticated user.
        """
        user = self.request.user
        if not user.is_authenticated():
            return []
        return Token.objects.filter(owner=user)

    def perform_create(self, serializer):

        # TODO : We should catch the event where the resulting token violates unique column constraint
        serializer.save(owner=self.request.user, token=binascii.hexlify(os.urandom(20)))
