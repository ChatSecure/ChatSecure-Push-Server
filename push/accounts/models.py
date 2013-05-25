from django.db import models
from django.contrib.auth.models import AbstractUser
from devices.models import Device


class PushUser(AbstractUser):
    devices = models.ManyToManyField(Device)
