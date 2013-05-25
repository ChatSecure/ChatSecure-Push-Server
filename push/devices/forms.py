from django.forms import ModelForm
from devices.models import AppleDevice


class AppleDeviceForm(ModelForm):
    class Meta:
        model = AppleDevice
        fields = ['device_type', 'operating_system', 'apple_push_token']
