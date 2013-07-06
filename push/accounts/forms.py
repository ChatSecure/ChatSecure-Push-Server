from django import forms


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()
    create = forms.BooleanField(required=False)
