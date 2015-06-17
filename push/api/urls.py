from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from tokens.views import TokenViewSet
from messages.views import MessagesViewSet
from accounts.views import AccountViewSet
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(prefix=r'device/apns', viewset=APNSDeviceAuthorizedViewSet)
router.register(prefix=r'device/gcm', viewset=GCMDeviceAuthorizedViewSet)
router.register(prefix=r'tokens', viewset=TokenViewSet, base_name='token')
router.register(prefix=r'messages', viewset=MessagesViewSet, base_name='message')
router.register(prefix=r'accounts', viewset=AccountViewSet, base_name='account')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
