from rest_framework import viewsets
from rest_framework import permissions
from tokens.models import WhitelistToken
from tokens.serializers import WhitelistTokenSerializer


class WhitelistTokenViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = WhitelistTokenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the devices
        for the currently authenticated user.
        """
        user = self.request.user
        return WhitelistToken.objects.filter(owner=user)

    def pre_save(self, obj):
        obj.owner = self.request.user