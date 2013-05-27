from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^device/', 'api.devices.register_device'),
    url(r'^account/', 'api.accounts.login_or_create_account'),

    url(r'^', 'api.views.root'),
)
