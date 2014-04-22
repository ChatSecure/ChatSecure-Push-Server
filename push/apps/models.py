from django.db import models
from oauth2_provider.models import AbstractApplication

class PushApplication(AbstractApplication):
    apns_dev = models.TextField(null=True, blank=True)
    apns_prod = models.TextField(null=True, blank=True)
    gcm_api_key = models.TextField(null=True, blank=True)
    itunes_shared_secret = models.CharField(max_length=50, null=True, blank=True)