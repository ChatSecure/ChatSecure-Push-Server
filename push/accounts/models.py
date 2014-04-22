from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.models import PushApplication


class PushUser(AbstractUser):
    expiration_date = models.DateField(null=True, blank=True)
    app = models.ForeignKey(PushApplication, null=True, blank=True, related_name='users')
