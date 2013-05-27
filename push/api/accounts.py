# Django
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import PushUser
import accounts.models as accounts
import json
from django.contrib.auth import authenticate, login


def check_email(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({'success': False, 'message': 'GET requests only'}), mimetype='application/json')
    email = request.GET.get('email', None)
    if not email:
        return HttpResponse(json.dumps({'success': False, 'message': 'Missing email key'}), mimetype='application/json')

    if accounts.email_available(email):
        return HttpResponse(json.dumps({'available': True}), mimetype='application/json')
    return HttpResponse(json.dumps({'available': False}), mimetype='application/json')


@csrf_exempt
def login_or_create_account(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'message': 'POST requests only'}), mimetype='application/json')
    email = request.GET.get('email', None)
    password = request.GET.get('password', None)

    if email is None or password is None:
        return HttpResponse(json.dumps({'success': False, 'message': 'Missing required parameters email or password'}), mimetype='application/json')

    user = accounts.user_for_email(email)
    success_message = 'Login Successful'
    if user is None:
        success_message = 'Account Creation Successful'
        user = PushUser.objects.create_user(username=email, email=email, password=password)

    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(json.dumps({'success': True, 'message': success_message}), mimetype='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'message': 'Account disabled'}), mimetype='application/json')
    else:
        return HttpResponse(json.dumps({'success': False, 'message': 'Invalid Login'}), mimetype='application/json')
