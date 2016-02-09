from __future__ import absolute_import

from celery import task
from messages.messenger import send_apns, send_gcm


@task(ignore_result=True)
def task_send_apns(registration_ids, message, **kwargs):
    return send_apns(registration_ids, message, **kwargs)


@task(ignore_result=True)
def task_send_gcm(registration_ids, message, **kwargs):
    return send_gcm(registration_ids, message, **kwargs)
