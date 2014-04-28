from rest_framework import viewsets
from rest_framework import permissions
from devices.models import Device
from devices.serializers import DeviceSerializer
from api.permissions import OwnerOnlyPermission


class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOnlyPermission)

    def get_queryset(self):
        """
        This view should return a list of all the devices
        for the currently authenticated user.
        """
        user = self.request.user
        return Device.objects.filter(owner=user)

    def pre_save(self, obj):
        obj.owner = self.request.user