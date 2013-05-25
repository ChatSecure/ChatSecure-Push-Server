from django.db import models
from django.contrib.auth.models import AbstractUser


class PushUser(AbstractUser):
    apple_devices = models.ManyToManyField('devices.AppleDevice')
