from django.db import models
from django.contrib.auth.models import AbstractUser


class PushUser(AbstractUser):
    apple_devices = models.ManyToManyField('devices.AppleDevice',blank=True, null=True)


def user_for_email(email=None):
    if email is None:
        return None
    user = None
    try:
        user = PushUser.objects.get(email=email)
    except:
        pass
    return user
