# Django
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import PermissionDenied
from devices.models import device_for_apple_push_token
from devices.forms import AppleDeviceForm
from devices.models import AppleDevice
from django.forms.models import model_to_dict


@csrf_exempt
def register_device(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'message': 'POST requests only'}), mimetype='application/json')
    if not request.user.is_authenticated():
        raise PermissionDenied

    apple_push_token = request.POST.get('apple_push_token', None)
    device = None
    if apple_push_token is not None:
        device = device_for_apple_push_token(apple_push_token)
        if device is None:
            device = AppleDevice()
            device.owner = request.user
        if device.owner is not request.user:
            raise PermissionDenied
        f = AppleDeviceForm(request.POST, instance=device)
        device = f.save()

    return HttpResponse(json.dumps({'success': True,
                                    'message': 'Device registration updated.',
                                    'object': model_to_dict(device, fields=[field.name for field in device._meta.fields])}),
                                    mimetype='application/json')
