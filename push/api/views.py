from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class PubSubNodeViewSet(GenericViewSet):
    """
    The "PubSub" Node is the broker between XMPP Servers and this ChatSecure Push instance's HTTP API.

    This API provides the address (XMPP JID) of the PubSub node which handles messages sent from an
    [XEP-0357](http://xmpp.org/extensions/xep-0357.html) capable XMPP Server and relays requests to the
    ChatSecure Push HTTP API as appropriate.

    ## Next Steps

    You typically provide the PubSub Node JID to your XMPP Server during the
    ["Enable Notifications"](http://xmpp.org/extensions/xep-0357.html#enabling) step defined in XEP-0357.

    For example, if using the excellent [RubDub](https://github.com/ChatSecure/RubDub) XMPP PubSub Node, your XMPP
    client would provide the `jid` returned from this API alongside a `push_whitelist_token` obtained from the
    [Token](/api/v1/tokens) API, to your XMPP server as follows:

    ```xml
        <iq type="set" id="enable1">
            <enable xmlns="urn:xmpp:push:0" jid="jid">
                <x xmlns="jabber:x:data">
                    <field var="FORM_TYPE"><value>http://jabber.org/protocol/pubsub#publish-options</value></field>
                    <field var="token"><value>push_whitelist_token</value></field>
                </x>
            </enable>
        </iq>
    ```

    """

    def list(self, request, *args, **kwargs):

        data = {
            'jid': settings.CHATSECURE_PUSH['XMPP_PUSH_SERVICE']
        }
        return Response(data)
