from django.db import models

# Create your models here.

class WhitelistToken(models.Model):
    token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    owner = models.ForeignKey('accounts.PushUser', related_name='tokens')
    app = models.ForeignKey('apps.PushApplication', related_name='tokens')
