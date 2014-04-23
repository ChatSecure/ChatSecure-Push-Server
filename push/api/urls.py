from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from devices.views import DeviceViewSet
from tokens.views import WhitelistTokenViewSet
from messages.views import MessagesViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(prefix=r'devices', viewset=DeviceViewSet, base_name='device')
router.register(prefix=r'tokens', viewset=WhitelistTokenViewSet, base_name='token')
router.register(prefix=r'messages', viewset=MessagesViewSet, base_name='message')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
