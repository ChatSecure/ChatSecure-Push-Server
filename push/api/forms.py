from django import forms


class KnockForm(forms.Form):
    email = forms.EmailField()


class MessageForm(forms.Form):
	email = forms.EmailField()
	text = forms.CharField(required=False)