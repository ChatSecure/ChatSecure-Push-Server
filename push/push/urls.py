from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

admin.autodiscover()


urlpatterns = [
    url(r'^api/', include(('api.urls', 'push'))),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]
