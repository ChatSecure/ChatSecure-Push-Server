from django.db import models
from django.contrib.auth.models import AbstractUser


class PushUser(AbstractUser):
    apple_devices = models.ManyToManyField('devices.AppleDevice')


def email_available(email=None):
    if email is None:
        return False
    if(len(PushUser.objects.filter(email=email)) < 1):
        return True
    return False
