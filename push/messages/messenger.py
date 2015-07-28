import collections
from push_notifications.apns import apns_send_bulk_message, apns_send_message
from push_notifications.gcm import gcm_send_bulk_message, gcm_send_message


def send_apns(registration_ids, message, **kwargs):
    '''
    Send a message to one or more APNS recipients

    :param registration_ids: a single or iterable collection of registration ids (APNS tokens)
    :param message: the payload to send. This is sent as the value of the 'alert' APNS key
    :param kwargs: additional APNS arguments. See push_notifications.apns._apns_sendd
    '''

    if isinstance(registration_ids, collections.Iterable):
        apns_send_bulk_message(registration_ids, message, **kwargs)
    else:
        apns_send_message(registration_ids, message, **kwargs)


def send_gcm(registration_ids, message, **kwargs):
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
