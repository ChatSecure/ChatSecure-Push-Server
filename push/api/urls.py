from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from devices.views import DeviceViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(prefix=r'devices', viewset=DeviceViewSet, base_name='device')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
