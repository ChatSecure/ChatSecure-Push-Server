# Django
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import email_available
import json


def check_email(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({'success': False, 'message': 'GET requests only'}), mimetype='application/json')
    email = request.GET.get('email', None)
    if not email:
        return HttpResponse(json.dumps({'success': False, 'message': 'Missing email key'}), mimetype='application/json')

    if email_available(email):
        return HttpResponse(json.dumps({'available': True}), mimetype='application/json')
    return HttpResponse(json.dumps({'available': False}), mimetype='application/json')


@csrf_exempt
def account(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'message': 'POST requests only'}), mimetype='application/json')
