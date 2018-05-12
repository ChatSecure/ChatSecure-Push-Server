from __future__ import absolute_import
from django import forms


class KnockForm(forms.Form):
    email = forms.EmailField()
