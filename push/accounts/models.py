from django.db import models
from django.contrib.auth.models import AbstractUser

class PushUser(AbstractUser):
    expiration_date = models.DateField(null=True, blank=True)
