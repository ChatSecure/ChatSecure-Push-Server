from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^device/', 'api.device.register_device'),
    url(r'^account/', 'api.account.view_account'),
    url(r'^knock/', 'api.views.knock'),
    url(r'^message/', 'api.message.send_message'),

    url(r'^', 'api.views.root'),
)
