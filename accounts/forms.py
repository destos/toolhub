from account import forms as account_forms
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from toolhub.forms import CrispyFormMixin


class LoginUsernameForm(CrispyFormMixin, account_forms.LoginUsernameForm):
    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'login'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Fieldset(
                'Login',
                Field('username'), Field('password'), Field('remember')
            ),
            Div(
                Div(
                    Submit('login', 'Login'),
                    css_class='col-md-offset-3 col-md-9'
                ),
                css_class='form-group'
            ))


class SignupForm(CrispyFormMixin, account_forms.SignupForm):
    # username, password, code and email provided by SignupForm
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'signup'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                'Account details',
                Field('username'), Field('email'), Field('password'),
                Field('password_confirm'), Field('code')
            ),
            Fieldset(
                'Extra Information',
                Field('first_name'), Field('last_name'),
            ),
            Div(
                Div(
                    Submit('register', 'Register'),
                    css_class='col-md-offset-2 col-md-10'
                ),
                css_class='form-group'
            ))

    def clean_email(self):
        email = super(SignupForm, self).clean_email()
        # email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'There is already a user with that email.')
        return email


class ChangePasswordForm(CrispyFormMixin, account_forms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'account:password'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Fieldset(
                _('Change password'),
                Field('password_current'),
                Field('password_new'),
                Field('password_new_confirm'),
                Div(
                    Div(
                        Submit('update', _('Update my password')),
                        css_class='col-md-offset-3 col-md-9'
                    ),
                    css_class='form-group'
                )))


class PasswordResetForm(CrispyFormMixin, account_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'account:password_reset'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        self.fields['email'].help_text = (_(
            "Forgotten your password? Enter your email address above,"
            " and we'll send you an email allowing you to reset it."))
        self.helper.layout = Layout(
            Fieldset(
                _('Reset password'),
                Field('email'),
                Div(
                    Div(
                        Submit('reset', _('Reset my password')),
                        css_class='col-md-offset-2 col-md-10'
                    ),
                    css_class='form-group'
                )))


class PasswordResetTokenForm(
        CrispyFormMixin, account_forms.PasswordResetTokenForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetTokenForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Fieldset(
                _('Set your new password'),
                Field('password'),
                Field('password_confirm'),
                Div(
                    Div(
                        Submit('reset', _('Update password')),
                        css_class='col-md-offset-3 col-md-9'
                    ),
                    css_class='form-group'
                )))


class SettingsForm(CrispyFormMixin, account_forms.SettingsForm):
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'account_settings'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Fieldset(
                _('Basic Information'),
                Field('email'), Field('timezone'), Field('language'),
                Div(
                    Div(
                        Submit('save', 'Save settings'),
                        css_class='col-md-offset-3 col-md-9'
                    ),
                    css_class='form-group'
                )))
