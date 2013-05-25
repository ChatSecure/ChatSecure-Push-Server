from django.db import models


class Device(models.Model):
    os_type = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey('accounts.PushUser')

    class Meta:
        abstract = True


class AppleDevice(Device):
    apple_push_token = models.CharField(max_length=64, null=True, blank=True)
