from account import views as account_views
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext as _

from accounts import forms


class ToolManager(TemplateView):
    pass


class SettingsView(account_views.SettingsView):
    template_name = 'accounts/settings.jinja'
    form_class = forms.SettingsForm

    def __init__(self, *args, **kwargs):
        super(SettingsView, self).__init__(*args, **kwargs)
        self.messages['email_changed'] = {
            "level": messages.INFO,
            "text": _("Email verification email send to your new email.")
        }

    def update_email(self, form, confirm=None):
        email = form.cleaned_data["email"].strip()
        if email != self.primary_email_address.email:
            messages.add_message(
                self.request,
                self.messages["email_changed"]["level"],
                self.messages["email_changed"]["text"]
            )
        super(SettingsView, self).update_email(form, confirm)


class LoginView(account_views.LoginView):
    template_name = 'accounts/login.jinja'
    form_class = forms.LoginUsernameForm


class LogoutView(account_views.LogoutView):

    def get_redirect_url(self):
        return reverse('base:home')

    # use the default post functionality, which is to logout and redirect
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


# TODO: create email confirmation template
class SignupView(account_views.SignupView):
    template_name = 'accounts/signup.jinja'
    # template_name_ajax = "account/ajax/signup.jinja"
    template_name_email_confirmation_sent = (
        "account/email_confirmation_sent.jinja")
    # template_name_email_confirmation_sent_ajax = (
    #     "account/ajax/email_confirmation_sent.jinja")
    template_name_signup_closed = "account/signup_closed.jinja"
    # template_name_signup_closed_ajax = "account/ajax/signup_closed.jinja"
    form_class = forms.SignupForm


class ConfirmEmailView(account_views.ConfirmEmailView):
    def get_template_names(self):
        return {
            'GET': ['accounts/email_confirm.jinja'],
            'POST': ['accounts/email_confirmed.jinja']
        }[self.request.method]

    def get_redirect_url(self):
        return reverse('account_settings')


class ChangePasswordView(account_views.ChangePasswordView):
    template_name = 'accounts/password_change.jinja'
    form_class = forms.ChangePasswordForm

    def get_success_url(self):
        return reverse('account_settings')


class PasswordResetView(account_views.PasswordResetView):
    template_name = 'accounts/password_reset.jinja'
    template_name_sent = 'accounts/password_reset_sent.jinja'
    form_class = forms.PasswordResetForm


class PasswordResetTokenView(account_views.PasswordResetTokenView):
    template_name = 'accounts/password_reset_token.jinja'
    template_name_fail = 'accounts/password_reset_token_fail.jinja'
    form_class = forms.PasswordResetTokenForm

    def get_success_url(self):
        return reverse('login')


class DeleteView(account_views.DeleteView):
    template_name = 'accounts/delete.jinja'


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.jinja'
    slug_field = 'username'
    model = User
    context_object_name = 'user'
