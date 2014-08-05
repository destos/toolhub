from account import views as account_views
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext as _

from accounts import forms
from lending.models import Transaction
from tools.models import UserTool
from toolhub.mixins import RestrictToUserMixin


class ToolManager(RestrictToUserMixin, ListView):
    template_name = 'accounts/tool_manager.jinja'
    restrict_user_field = 'owner'
    model = UserTool


class LendingManager(RestrictToUserMixin, SingleObjectMixin, TemplateView):
    template_name = 'accounts/lending_manager.jinja'
    restrict_user_field = 'lendee'
    context_object_name = 'lent_to_user'
    object = None

    def get_queryset(self):
        """
        Filtered to only transaction requests made by user
        by RestrictToUserMixin
        """
        self.queryset = Transaction.objects.active()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'requests': self.get_requests(),
            'lending': self.get_lending()
        }
        context.update(kwargs)
        return super(LendingManager, self).get_context_data(**context)

    def get_initiating_queryset(self):
        """
        Transactions that have been initiated by other users related to
        owned tools
        """
        return Transaction.objects.filter(tool__owner=self.request.user)

    def get_requests(self):
        """
        Tools that others are requesting of the current user.
        """
        return self.get_initiating_queryset().request_open()

    def get_lending(self):
        """
        Tools that are currently being lent from the current user.
        """
        return self.get_initiating_queryset().active()


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
    redirect_field_name = 'return'


class LogoutView(account_views.LogoutView):

    def get_redirect_url(self):
        return reverse('homepage')

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
        return reverse('account:settings')


class ChangePasswordView(account_views.ChangePasswordView):
    template_name = 'accounts/password_change.jinja'
    form_class = forms.ChangePasswordForm

    def get_success_url(self):
        return reverse('account:settings')


class PasswordResetView(account_views.PasswordResetView):
    template_name = 'accounts/password_reset.jinja'
    template_name_sent = 'accounts/password_reset_sent.jinja'
    form_class = forms.PasswordResetForm


class PasswordResetTokenView(account_views.PasswordResetTokenView):
    template_name = 'accounts/password_reset_token.jinja'
    template_name_fail = 'accounts/password_reset_token_fail.jinja'
    form_class = forms.PasswordResetTokenForm

    def get_success_url(self):
        return reverse('account:login')


class DeleteView(account_views.DeleteView):
    template_name = 'accounts/delete.jinja'


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.jinja'
    slug_field = 'username'
    model = User
    context_object_name = 'user'
