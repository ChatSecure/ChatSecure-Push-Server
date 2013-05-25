from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^device/', 'api.devices.register_device'),
    url(r'^', 'api.views.root'),
)
