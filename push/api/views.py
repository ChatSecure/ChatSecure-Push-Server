from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts import models as accounts
from api.tasks import apns_push
from api.forms import KnockForm


@csrf_exempt
def knock(request):
    form = KnockForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps({'success': False, 'message': form.errors}), mimetype='application/json')

    email = form.cleaned_data.get('email', None)
    user = accounts.user_for_email(email)
    apple_devices = user.apple_devices.all()

    apple_tokens = []

    for device in apple_devices:
        apple_tokens.append(device.apple_push_token)

    if len(apple_tokens) > 0:
        apns_push.delay(tokens=apple_tokens, message="Someone requested an OTR conversation!")
    return HttpResponse(json.dumps({'success': True, 'message': 'Sent the message'}), mimetype='application/json')


@csrf_exempt
def root(request):
    return HttpResponse(json.dumps({'success': True, 'message': 'ChatSecure Push API v1.0'}), mimetype='application/json')
