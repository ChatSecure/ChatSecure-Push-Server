from __future__ import absolute_import

from celery import shared_task
from messages.messenger import send_apns, send_gcm

@shared_task
def task_send_apns(registration_ids, message, **kwargs):
    return send_apns(registration_ids, message, **kwargs)

@shared_task
def task_send_gcm(registration_ids, message, **kwargs):
    return send_gcm(registration_ids, message, **kwargs)
