from rest_framework import viewsets
from rest_framework import permissions
from tokens.models import Token
from tokens.serializers import TokenSerializer
import binascii
import os


class TokenViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = TokenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the devices
        for the currently authenticated user.
        """
        user = self.request.user
        return Token.objects.filter(owner=user)

    def pre_save(self, obj):
        obj.owner = self.request.user
        if not obj.token:
            obj.token = binascii.hexlify(os.urandom(20))
