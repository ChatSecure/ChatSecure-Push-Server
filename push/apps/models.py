from django.db import models
from oauth2_provider.models import AbstractApplication

class PushApplication(AbstractApplication):
    apns_dev = models.TextField()
    apns_prod = models.TextField()
    gcm_api_key = models.TextField()
    itunes_shared_secret = models.CharField(max_length=50, null=True, blank=True)