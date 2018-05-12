from __future__ import absolute_import
from django.conf.urls import include, url
from api.routers import Router
from api.views import PubSubNodeViewSet
from tokens.views import TokenViewSet
from messages.views import MessagesViewSet
from accounts.views import AccountViewSet
from devices.views import GCMDeviceAuthorizedViewSet, APNSDeviceAuthorizedViewSet

# Create a router and register our viewsets with it.
router = Router()
router.register(prefix=r'device/apns', viewset=APNSDeviceAuthorizedViewSet)
router.register(prefix=r'device/gcm', viewset=GCMDeviceAuthorizedViewSet)
router.register(prefix=r'tokens', viewset=TokenViewSet, base_name='token')
router.register(prefix=r'messages', viewset=MessagesViewSet, base_name='message')
router.register(prefix=r'accounts', viewset=AccountViewSet, base_name='account')
router.register(prefix=r'pubsub', viewset=PubSubNodeViewSet, base_name='pubsub')

urlpatterns = [
    url(r'^v1/', include((router.urls, 'push'), namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
