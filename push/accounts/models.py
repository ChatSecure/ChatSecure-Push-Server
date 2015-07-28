import uuid
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class PushUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    expiration_date = models.DateField(null=True, blank=True)


def create_auth_token_for_user(sender, instance, created, **kwargs):
    '''
    Create an auth token for Django Rest Framework's TokenAuthentication
    for this user. This token is required for SDK API access.
    '''
    if created:
        Token.objects.create(user=instance)


# register the signal
post_save.connect(create_auth_token_for_user, sender=PushUser)
# not post save, only on create