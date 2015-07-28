# coding=utf-8
import uuid
from django.db import models
from django.utils.translation import ugettext as _
from push import settings


# Abstract model class
class Device(models.Model):
    '''
    Abstract class representing a pushable device. Implementation classes must add
    an 'owner' field.
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    active = models.BooleanField(verbose_name=_("Is active"), default=True,
                                 help_text=_("Inactive devices will not be sent notifications"))

    # owner field provided by implementation class, for unique 'related_name' kwarg
    date_created = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True, null=True)

    registration_id = models.TextField(verbose_name=_("Registration ID"))
    device_id = models.TextField(verbose_name=_("Device ID"), blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name or \
               str(self.device_id or "") or \
               "%s for %s" % (self.__class__.__name__, self.owner or "unknown owner")


class GCMDevice(Device):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='gcm_devices')

    class Meta:
        verbose_name = _("GCM device")


class APNSDevice(Device):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='apns_devices')

    class Meta:
        verbose_name = _("APNS device")
