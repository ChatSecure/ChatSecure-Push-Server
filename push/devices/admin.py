from django.contrib import admin
from devices.models import GCMDevice, APNSDevice
from push_notifications.models import APNSDevice as PNAPNSDevice, GCMDevice as PNGCMDevice

admin.site.register(GCMDevice)
admin.site.register(APNSDevice)

# Remove push-notifications entries until we remove the library entirely
admin.site.unregister(PNAPNSDevice)
admin.site.unregister(PNGCMDevice)