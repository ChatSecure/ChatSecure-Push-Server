# Django
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import PushUser
from accounts import models as accounts
import json
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm


@csrf_exempt
def view_account(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'message': 'POST requests only'}), mimetype='application/json')
    form = LoginForm(request.POST)

    if not form.is_valid():
        return HttpResponse(json.dumps({'success': False, 'message': form.errors}), mimetype='application/json')

    email = form.cleaned_data.get('email', None)
    password = form.cleaned_data.get('password', None)
    create = form.cleaned_data.get('create', False)

    if email is None or password is None:
        return HttpResponse(json.dumps({'success': False, 'message': 'Missing required parameters email or password'}), mimetype='application/json')

    user = accounts.user_for_email(email)
    success_message = 'Login Successful'
    if user is None and create is True:
        success_message = 'Account Creation Successful'
        user = PushUser.objects.create_user(username=email, email=email, password=password)

    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(json.dumps({'success': True, 'message': success_message}), mimetype='application/json')
    return HttpResponse(json.dumps({'success': False, 'message': 'Invalid Login'}), mimetype='application/json')
