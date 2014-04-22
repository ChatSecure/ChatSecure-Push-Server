from django.db import models
from django.conf import settings


class Device(models.Model):
    OS_IOS = 'iOS'
    OS_ANDROID = 'Android'
    OS_TYPE_CHOICES = (
        (OS_IOS, OS_IOS),
        (OS_ANDROID, OS_ANDROID),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='devices')
    os_type = models.CharField(u'Operating System Type',
                               max_length=255,
                               choices=OS_TYPE_CHOICES)
    os_version = models.CharField(u'Operating System Version',
                                  max_length=255,
                                  null=True,
                                  blank=True)
    device_name = models.CharField(u'Device Name',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    push_token = models.CharField(u'Push Token',
                                  max_length=255)