from __future__ import absolute_import
from django.contrib import admin
from devices.models import GCMDevice, APNSDevice
from push_notifications.models import APNSDevice as PNAPNSDevice, GCMDevice as PNGCMDevice


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'owner', 'date_created',)
    readonly_fields = ('date_created', 'name', 'device_id', 'active',)
    search_fields = ['registration_id', 'owner__username']
    raw_id_fields = ['owner']
    ordering = ('-date_created',)


admin.site.register(GCMDevice, DeviceAdmin)
admin.site.register(APNSDevice, DeviceAdmin)

# Remove push-notifications entries until we remove the library entirely
admin.site.unregister(PNAPNSDevice)
admin.site.unregister(PNGCMDevice)
