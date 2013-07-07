from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts import models as accounts
from devices.models import AppleDevice
from api.tasks import apns_push


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
        apns_push.delay(tokens=apple_tokens, message="Someone requested an OTR conversation!")
    return HttpResponse(json.dumps({'success': True, 'message': 'Sent the message'}), mimetype='application/json')


@csrf_exempt
def root(request):
    return HttpResponse(json.dumps({'success': True, 'message': 'ChatSecure Push API v1.0'}), mimetype='application/json')
