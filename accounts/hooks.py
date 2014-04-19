from account.hooks import AccountDefaultHookSet
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


class AccountHookSet(AccountDefaultHookSet):
    def send_invitation_email(self, to, ctx):
        subject = render_to_string(
            "accounts/email/invite_user_subject.txt", ctx)
        message = render_to_string("accounts/email/invite_user.txt.jinja", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_confirmation_email(self, to, ctx):
        subject = render_to_string(
            "accounts/email/email_confirmation_subject.txt.jinja", ctx)
        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "accounts/email/email_confirmation_message.txt.jinja", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_change_email(self, to, ctx):
        subject = render_to_string(
            "accounts/email/password_change_subject.txt.jinja", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "accounts/email/password_change.txt.jinja", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_reset_email(self, to, ctx):
        subject = render_to_string(
            "accounts/email/password_reset_subject.txt.jinja", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "accounts/email/password_reset.txt.jinja", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
