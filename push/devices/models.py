from django.db import models


class AbstractDevice(models.Model):
    device_type = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    device_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

class AppleDevice(AbstractDevice):
    owner = models.ForeignKey('accounts.PushUser', related_name='apple_devices')
    apns_token = models.CharField(max_length=64, null=True, blank=True)

class AndroidDevice(AbstractDevice):
    owner = models.ForeignKey('accounts.PushUser', related_name='android_devices')
    notification_key = models.CharField(max_length=64, null=True, blank=True)
