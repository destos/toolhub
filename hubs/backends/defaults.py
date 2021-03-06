import uuid

from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, get_user_model, login
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import Context, loader
from django.utils.translation import ugettext as _

from .tokens import RegistrationTokenGenerator
from .forms import UserRegistrationForm, HubRegistrationForm
from hubs.utils import create_hub, model_field_attr


# Backend classes should provide common interface
class BaseBackend(object):
    """
    Base backend class for registering and inviting users to an hub
    """

    def __init__(self, *args, **kwargs):
        self.user_model = get_user_model()

    def get_urls(self):
        raise NotImplementedError

    def get_success_url(self):
        """Will return the class's `success_url` attribute unless overridden"""
        raise NotImplementedError

    def get_form(self, **kwargs):
        """Returns the form for registering or inviting a user"""
        if not hasattr(self, 'form_class'):
            raise AttributeError(_("You must define a form_class"))
        return self.form_class(**kwargs)

    def get_token(self, user, **kwargs):
        """Returns a unique token for the given user"""
        return RegistrationTokenGenerator().make_token(user)

    def get_username(self):
        """Returns a UUID based 'random' and unique username"""
        return str(uuid.uuid4())[:model_field_attr(
            self.user_model, 'username', 'max_length')]

    def activate_view(self, request, user_id, token):
        """
        Activates the given User by setting `is_active` to true if the provided
        information is verified.
        """
        try:
            user = self.user_model.objects.get(id=user_id, is_active=False)
        except self.user_model.DoesNotExist:
            raise Http404(_("Your URL may have expired."))
        if not RegistrationTokenGenerator().check_token(user, token):
            raise Http404(_("Your URL may have expired."))
        form = self.get_form(data=request.POST or None, instance=user)
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            for org in user.hub_set.filter(is_active=False):
                org.is_active = True
                org.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            login(request, user)
            return redirect(self.get_success_url())
        return render(request, 'hubs/register_form.jinja', {'form': form})

    def send_reminder(self, user, sender=None, **kwargs):
        """Sends a reminder email to the specified user"""
        if user.is_active:
            return False
        token = RegistrationTokenGenerator().make_token(user)
        kwargs.update({'token': token})
        self._send_email(
            user, self.reminder_subject, self.reminder_body, sender, **kwargs)

    def _send_email(
            self, user, subject_template, body_template,
            sender=None, **kwargs):
        """Utility method for sending emails to new users"""
        if sender:
            from_email = "%s %s <%s>" % (
                sender.first_name, sender.last_name,
                settings.DEFAULT_FROM_EMAIL)
            reply_to = "%s %s <%s>" % (
                sender.first_name, sender.last_name, sender.email)
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = from_email

        headers = {'Reply-To': reply_to}
        kwargs.update({'sender': sender, 'user': user})
        ctx = Context(kwargs, autoescape=False)

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(ctx).strip()
        body = body_template.render(ctx)
        return EmailMessage(
            subject, body, from_email, [user.email], headers=headers).send()


class RegistrationBackend(BaseBackend):
    """
    A backend for allowing new users to join the site by creating a new user
    associated with a new hub.
    """
    # NOTE this backend stands to be simplified further, as email verification
    # should be beyond the purview of this app
    activation_subject = 'hubs/email/activation_subject.txt'
    activation_body = 'hubs/email/activation_body.jinja'
    reminder_subject = 'hubs/email/reminder_subject.txt'
    reminder_body = 'hubs/email/reminder_body.jinja'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('registration_success')

    def get_urls(self):
        return patterns(
            '',
            url(r'^complete/$',
                view=self.success_view,
                name="registration_success"),
            url(r'^(?P<user_id>[\d]+)-'
                '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="registration_register"),
            url(r'^$', view=self.create_view, name="registration_create"),
        )

    def register_by_email(self, email, sender=None, request=None, **kwargs):
        """
        Returns a User object filled with dummy data and not active, and sends
        an invitation email.
        """
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(
                username=self.get_username(),
                email=email,
                password=self.user_model.objects.make_random_password())
            user.is_active = False
            user.save()
        self.send_activation(user, sender, **kwargs)
        return user

    def send_activation(self, user, sender=None, **kwargs):
        """
        Invites a user to join the site
        """
        if user.is_active:
            return False
        token = self.get_token(user)
        kwargs.update({'token': token})
        self._send_email(
            user, self.activation_subject, self.activation_body,
            sender, **kwargs)

    def create_view(self, request):
        """
        Initiates the hub and user account creation process
        """
        if request.user.is_authenticated():
            return redirect("hubs:add")
        form = HubRegistrationForm(request.POST or None)
        if form.is_valid():
            try:
                user = self.user_model.objects.get(
                    email=form.cleaned_data['email'])
            except self.user_model.DoesNotExist:
                user = self.user_model.objects.create(
                    username=self.get_username(),
                    email=form.cleaned_data['email'],
                    password=self.user_model.objects.make_random_password())
                user.is_active = False
                user.save()
            else:
                return redirect("hubs:add")
            hub = create_hub(
                user, form.cleaned_data['name'],
                form.cleaned_data['slug'], is_active=False)
            return render(
                request, 'hubs/register_success.jinja',
                {'user': user, 'hub': hub})
        return render(
            request, 'hubs/register_form.jinja',
            {'form': form})

    def success_view(self, request):
        return render(request, 'hubs/register_success.jinja', {})


class InvitationBackend(BaseBackend):
    """
    A backend for inviting new users to join the site as members of a
    hub.
    """
    invitation_subject = 'hubs/email/invitation_subject.txt'
    invitation_body = 'hubs/email/invitation_body.jinja'
    reminder_subject = 'hubs/email/reminder_subject.txt'
    reminder_body = 'hubs/email/reminder_body.jinja'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('hub_list')

    def get_urls(self):
        return patterns(
            '',
            url(r'^(?P<user_id>[\d]+)-'
                '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="invitations_register"),
        )

    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        """Creates an inactive user with the information we know and then sends
        an invitation email for that user to complete registration.

        If your project uses email in a different way then you should make to
        extend this method as it only checks the `email` attribute for Users.
        """
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(
                username=self.get_username(),
                email=email,
                password=self.user_model.objects.make_random_password())
            user.is_active = False
            user.save()
        self.send_invitation(user, sender, **kwargs)
        return user

    def send_invitation(self, user, sender=None, **kwargs):
        """An intermediary function for sending an invitation email that
        selects the templates, generating the token, and ensuring that the user
        has not already joined the site.
        """
        if user.is_active:
            return False
        token = self.get_token(user)
        kwargs.update({'token': token})
        self._send_email(
            user, self.invitation_subject, self.invitation_body,
            sender, **kwargs)
