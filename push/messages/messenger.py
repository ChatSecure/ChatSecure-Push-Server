import collections
import logging

from push_notifications.apns import apns_send_bulk_message, apns_send_message
from push_notifications.gcm import gcm_send_bulk_message, gcm_send_message
from push.celery import app
from django.conf import settings


USE_MESSAGE_QUEUE = settings.CHATSECURE_PUSH['USE_MESSAGE_QUEUE']

logger = logging.getLogger("django")


def send_apns(registration_ids, message, **kwargs):
    if USE_MESSAGE_QUEUE:
        _task_send_apns(registration_ids, message, **kwargs)
    else:
        _send_apns(registration_ids, message, **kwargs)


def send_gcm(registration_ids, message, **kwargs):
    if USE_MESSAGE_QUEUE:
        _task_send_gcm(registration_ids, message, **kwargs)
    else:
        _send_gcm(registration_ids, message, **kwargs)


def _send_apns(registration_ids, message, **kwargs):
    '''
    Send a message to one or more APNS recipients

    :param registration_ids: a single or iterable collection of registration ids (APNS tokens)
    :param message: the payload to send. This is sent as the value of the 'alert' APNS key
    :param kwargs: additional APNS arguments. See push_notifications.apns._apns_sendd
    '''

    try:
        if isinstance(registration_ids, collections.Iterable):
            apns_send_bulk_message(registration_ids, message, **kwargs)
        else:
            apns_send_message(registration_ids, message, **kwargs)
    except Exception as exception:
        logger.info("Exception sending APNS message: %s" % str(exception))


def _send_gcm(registration_ids, message, **kwargs):
    '''
    Send a message to one or more GCM recipients

    :param registration_ids: a single or iterable collection of registraion ids (GCM tokens)
    :param message: the payload to send. This is sent as the value of the 'message' GCM key,
    itself within the 'extra' key.
    :param kwargs: additional GCM arguments. Currently inserted directly into the payload
    '''

    data = kwargs.pop("extra", {})

    if message is not None:
        data["message"] = message

    if isinstance(registration_ids, collections.Iterable):
        gcm_send_bulk_message(registration_ids, data, **kwargs)
    else:
        gcm_send_message(registration_ids, data, **kwargs)


@app.task(ignore_result=True)
def _task_send_apns(registration_ids, message, **kwargs):
    return _send_apns(registration_ids, message, **kwargs)


@app.task(ignore_result=True)
def _task_send_gcm(registration_ids, message, **kwargs):
    return _send_gcm(registration_ids, message, **kwargs)
