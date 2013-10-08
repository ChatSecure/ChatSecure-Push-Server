from django.db import models
from django.contrib.auth.models import AbstractUser
from api.tasks import apns_push


class PushUser(AbstractUser):
    apple_devices = models.ManyToManyField('devices.AppleDevice',blank=True, null=True)


    def send_message(self,recipient=None,text=None):
    	for device in recipient.apple_devices:
    		apns_push.delay(device.apple_push_token,text)

def user_for_email(email=None):
    if email is None:
        return None
    user = None
    try:
        user = PushUser.objects.get(email=email)
    except:
        pass
    return user
