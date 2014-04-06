from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _

from .models import Hub, HubUser
from .utils import create_hub
from .backends import InvitationBackend


class HubForm(forms.ModelForm):
    """Form class for updating Hubs"""
    owner = forms.ModelChoiceField(HubUser.objects.all())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(HubForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = self.instance.hub_users.filter(
            is_admin=True, user__is_active=True)
        self.fields['owner'].initial = self.instance.owner.hub_user

    class Meta:
        model = Hub
        exclude = ('users', 'is_enabled')

    def save(self, commit=True):
        if self.instance.owner.hub_user != self.cleaned_data['owner']:
            self.instance.owner.hub_user = self.cleaned_data['owner']
            self.instance.owner.save()
        return super(HubForm, self).save(commit=commit)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        if owner != self.instance.owner.hub_user:
            if self.request.user != self.instance.owner.hub_user.user:
                raise forms.ValidationError(
                    _("Only the hub owner can change ownerhip"))
        return owner


class HubUserForm(forms.ModelForm):
    """Form class for updating HubUsers"""

    class Meta:
        model = HubUser
        exclude = ('hub', 'user')

    def clean_is_admin(self):
        is_admin = self.cleaned_data['is_admin']
        if self.instance.hub.owner.hub_user == self.instance and not is_admin:
            raise forms.ValidationError(_("The hub owner must be an admin"))
        return is_admin


class HubUserAddForm(forms.ModelForm):
    """Form class for adding HubUsers to an existing Hub"""
    email = forms.EmailField(max_length=75)

    def __init__(self, request, hub, *args, **kwargs):
        self.request = request
        self.hub = hub
        super(HubUserAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HubUser
        exclude = ('user', 'hub')

    def save(self, *args, **kwargs):
        """
        The save method should create a new HubUser linking the User
        matching the provided email address. If not matching User is found it
        should kick off the registration process. It needs to create a User in
        order to link it to the Hub.
        """
        try:
            user = get_user_model().objects.get(
                email__iexact=self.cleaned_data['email'])
        except get_user_model().MultipleObjectsReturned:
            raise forms.ValidationError(
                _("This email address has been used multiple times."))
        except get_user_model().DoesNotExist:
            user = InvitationBackend().invite_by_email(
                self.cleaned_data['email'],
                **{'domain': get_current_site(self.request),
                    'hub': self.hub})
        return HubUser.objects.create(
            user=user, hub=self.hub, is_admin=self.cleaned_data['is_admin'])

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.hub.users.filter(email=email):
            raise forms.ValidationError(_("There is already an hub "
                                          "member with this email address!"))
        return email


class HubAddForm(forms.ModelForm):
    """
    Form class for creating a new hub, complete with new owner, including a
    User instance, HubUser instance, and HubOwner instance.
    """
    email = forms.EmailField(
        max_length=75, help_text=_("The email address for the account owner"))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(HubAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Hub
        exclude = ('users', 'is_enabled')

    def save(self, **kwargs):
        """
        Create the hub, then get the user, then make the owner.
        """
        is_enabled = True
        try:
            user = get_user_model().objects.get(
                email=self.cleaned_data['email'])
        except get_user_model().DoesNotExist:
            user = InvitationBackend().invite_by_email(
                self.cleaned_data['email'],
                **{'domain': get_current_site(self.request),
                    'hub': self.cleaned_data['name'],
                    'sender': self.request.user, 'created': True})
            is_enabled = False
        return create_hub(
            user, self.cleaned_data['name'],
            self.cleaned_data['slug'], is_enabled=is_enabled)


class SignUpForm(forms.Form):
    """
    From class for signing up a new user and new account.
    """
    name = forms.CharField(
        max_length=50, help_text=_("The name of the hub"))
    # TODO don't need, as auto generated is better, add private/public toggle
    slug = forms.SlugField(
        max_length=50,
        help_text=_("The name in all lowercase, "
                    "suitable for URL identification"))
    email = forms.EmailField()
