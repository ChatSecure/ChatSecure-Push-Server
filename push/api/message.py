
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
import json
from accounts import models as accounts
from api.tasks import apns_push
from api.forms import MessageForm



@require_POST
@csrf_exempt
def send_message(request):
	if not request.user.is_authenticated():
		raise PermissionDenied
	#print request

	params = json.loads(request.body)

	form = MessageForm(params)

	if not form.is_valid():
		return HttpResponse(json.dumps({'success': False, 'message': form.errors}), mimetype='application/json')
	else:
		print form.data

	email = form.cleaned_data.get('email', None)
	text = form.cleaned_data.get('text',None)
	if email is None or text is None:
		return HttpResponse(json.dumps({'success': False, 'message': 'missing data'}), mimetype='application/json')

	recipient = accounts.user_for_email(email)
	if recipient is None:
		return HttpResponse(json.dumps({'success': False, 'message': 'Unknown User'}), mimetype='application/json')

	apple_devices = recipient.apple_devices.all()
	apple_tokens = []

	for device in apple_devices:
		apple_tokens.append(device.apple_push_token)

	if len(apple_tokens) > 0:
		#apns_push.delay(tokens=apple_tokens, message=text, sender=request.user.username,recipient=email)
		apns_push.delay(tokens=apple_tokens, message=text, sender='davidchiles@swissjabber.eu',recipient='fake.david.chiles@gmail.com')
	return HttpResponse(json.dumps({'success': True, 'message': 'Sent the message'}), mimetype='application/json')



