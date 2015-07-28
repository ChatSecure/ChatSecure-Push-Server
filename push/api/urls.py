from django.conf.urls import patterns, include, url
from api.routers import Router
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

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls, namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
