from django.db import models
from oauth2_provider.models import AbstractApplication


class PushApplication(AbstractApplication):
    apns_dev = models.TextField('APNS Development Certificate', null=True, blank=True)
    apns_prod = models.TextField('APNS Production Certificate', null=True, blank=True)
    gcm_api_key = models.TextField('Google Cloud Messaging API Key', null=True, blank=True)
    itunes_shared_secret = models.CharField('iTunes Shared Secret', max_length=50, null=True, blank=True)