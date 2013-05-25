from django.db import models


class Device(models.Model):
    device_type = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey('accounts.PushUser')

    class Meta:
        abstract = True


class AppleDevice(Device):
    apple_push_token = models.CharField(max_length=64, null=True, blank=True)


def device_for_apple_push_token(apple_push_token=None):
    if apple_push_token is None:
        return None
    device = None
    try:
        device = AppleDevice.objects.get(apple_push_token=apple_push_token)
    except:
        pass
    return device
