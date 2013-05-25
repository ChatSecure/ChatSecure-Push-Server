from django.shortcuts import HttpResponse
import json


def root(request):
    return HttpResponse(json.dumps({'success': True, 'message': 'ChatSecure Push API v1.0'}), mimetype='application/json')
