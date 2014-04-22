from django.contrib import admin
from accounts.models import PushUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import forms


# http://stackoverflow.com/questions/16953302/django-custom-user-model-in-admin-relation-auth-user-does-not-exist
class PushUserCreationForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            PushUser._default_manager.get(username=username)
        except PushUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = PushUser


# http://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model
class PushUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = PushUser


class PushUserAdmin(UserAdmin):
    form = PushUserChangeForm
    add_form = PushUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('expiration_date',)}),
    )

admin.site.register(PushUser, PushUserAdmin)
