from django.db import models
from accounts.models import PushUser
from apps.models import PushApplication


class WhitelistToken(models.Model):
    token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    owner = models.ForeignKey(PushUser, related_name='tokens')
    app = models.ForeignKey(PushApplication, related_name='tokens')
