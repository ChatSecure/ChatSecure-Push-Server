from django import forms


class KnockForm(forms.Form):
    email = forms.EmailField()
