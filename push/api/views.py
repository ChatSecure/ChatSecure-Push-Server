from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts import models as accounts
from apnsclient import *
from push import settings
from devices.models import AppleDevice

# For feedback or non-intensive messaging
con = Session.new_connection("feedback_sandbox", cert_file=settings.APNS_DEV_CERT_PATH, passphrase=settings.APNS_DEV_PASSPHRASE)

# Persistent connection for intensive messaging.
# Keep reference to session instance in some class static/global variable,
# otherwise it willbe garbage collected and all connections will be closed.
session = Session()
con = session.get_connection("push_sandbox", cert_file=settings.APNS_DEV_CERT_PATH, passphrase=settings.APNS_DEV_PASSPHRASE)


@csrf_exempt
def knock(request):
    email = request.GET.get('email', None)
    print 'email: ' + str(email)
    user = accounts.user_for_email(email)
    print 'user : ' + str(user)
    apple_devices = user.apple_devices.all()
    print 'users devices: ' + str(apple_devices)

    apple_devices = AppleDevice.objects.all()
    print 'all devices: ' + str(apple_devices)

    apple_tokens = []

    for device in apple_devices:
        apple_tokens.append(device.apple_push_token)



    if len(apple_tokens) > 0:
        print 'pushing to : ' + str(apple_tokens)
        # New message to 3 devices. You app will show badge 10 over app's icon.
        message = Message(apple_tokens, alert="Someone requested an OTR conversation!", badge=1)

        # Send the message.
        srv = APNs(con)
        res = srv.send(message)

        # Check failures. Check codes in APNs reference docs.
        for token, reason in res.failed.items():
            code, errmsg = reason
            print "Device faled: {0}, reason: {1}".format(token, errmsg)

        # Check failures not related to devices.
        for code, errmsg in res.errors:
            print "Error: ", errmsg

        # Check if there are tokens that can be retried
        if res.needs_retry():
            # repeat with retry_message or reschedule your task
            retry_message = res.retry()
    return HttpResponse(json.dumps({'success': True, 'message': 'Sent the message'}), mimetype='application/json')



@csrf_exempt
def root(request):
    return HttpResponse(json.dumps({'success': True, 'message': 'ChatSecure Push API v1.0'}), mimetype='application/json')
