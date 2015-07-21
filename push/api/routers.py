from django.core.urlresolvers import NoReverseMatch
from rest_framework import views
from rest_framework.compat import get_resolver_match, OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter


class Router(DefaultRouter):
    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            """
            ChatSecure Push provides application agnostic and privacy-conscious push messaging for APNS and GCM devices.
            This application currently implements the [Level 1](https://github.com/ChatSecure/ChatSecure-Push-Server/blob/master/docs/v3/README.md#level-1)
            protocol.

            # Flow

            #### 1. Create an [Account](/api/accounts/).

            + The Account create response will include an HTTP Authorization token required for the following requests.

            #### 2. Create a [GCM](/api/device/gcm/) or [APNS](/api/device/apns) device.
            #### 3. Create a [Token](/api/tokens/) to allow others to send push messages to your device.
            #### 4. When you receive another's Token, send them a [Message](/api/messages)
            """
            _ignore_model_permissions = True

            def get(self, request, *args, **kwargs):
                ret = OrderedDict()
                namespace = get_resolver_match(request).namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse(
                            url_name,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                    except NoReverseMatch:
                        # Don't bail out if eg. no list routes exist, only detail routes.
                        continue

                return Response(ret)

        return APIRoot.as_view()