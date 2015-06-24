from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from rest_framework.relations import RelatedField
from push_notifications.models import GCMDevice, APNSDevice

__author__ = 'davidbrodsky'


class RegistrationIdRelatedField(RelatedField):

    default_error_messages = {
        'required': 'This field is required.',
        'does_not_exist': 'Invalid registration_id "{registration_id}" - object does not exist.',
        'incorrect_type': 'Incorrect type. Expected registration_id value, received {data_type}.',
    }

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(registration_id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', registration_id=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return value.registration_id
