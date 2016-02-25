from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from devices.models import APNSDevice, GCMDevice


class Token(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(verbose_name=_('Whitelist Token'), max_length=100, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens')
    apns_device = models.ForeignKey(APNSDevice, blank=True, null=True)
    gcm_device = models.ForeignKey(GCMDevice, blank=True, null=True)
    # null=True so tokens created before migration can exist
    date_created = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True, null=True)

    def __unicode__(self):
        owner_name = self.owner.username
        token_type = "APNS" if self.apns_device is not None else "GCM"
        return "%s's %s token created %s" % (owner_name, token_type, self.date_created)
