from django.db import models
from django.conf import settings


class WhitelistToken(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField('Whitelist Token', max_length=100, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens')