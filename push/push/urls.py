from django.conf.urls import include, url
from django.contrib import admin
from acme.views import acme_challenge

admin.autodiscover()

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'.well-known/acme-challenge/(?P<token>.+)', acme_challenge),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
