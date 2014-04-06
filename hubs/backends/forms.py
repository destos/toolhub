from django import forms
from django.contrib.auth import get_user_model
from hubs.models import Hub


class UserRegistrationForm(forms.ModelForm):
    """Form class for completing a user's registration and activating the
    User."""
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.initial['username'] = ''

    class Meta:
        model = get_user_model()
        exclude = ('is_staff', 'is_superuser', 'is_active', 'last_login',
                   'date_joined', 'groups', 'user_permissions')


class HubRegistrationForm(forms.ModelForm):
    """Form class for creating new organizations owned by new users."""
    email = forms.EmailField()

    class Meta:
        model = Hub
        exclude = ('is_active', 'users')

    def save(self, *args, **kwargs):
        self.instance.is_active = False
        super(HubRegistrationForm, self).save(*args, **kwargs)
