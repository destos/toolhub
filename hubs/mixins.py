from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from hubs.models import Hub, HubUser


class HubMixin(object):
    """Mixin used like a SingleObjectMixin to fetch an hub"""

    hub_model = Hub
    hub_context_name = 'hub'

    def get_hub_model(self):
        return self.hub_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.hub_context_name: self.get_hub()})
        return super(HubMixin, self).get_context_data(**kwargs)

    def get_object(self):
        if hasattr(self, 'hub'):
            return self.hub
        hub_slug = self.kwargs.get('hub_slug', None)
        self.hub = get_object_or_404(self.get_hub_model(), slug=hub_slug)
        return self.hub

    get_hub = get_object  # Now available when `get_object` is overridden


class HubUserMixin(HubMixin):
    """Mixin used like a SingleObjectMixin to fetch an hub user"""

    user_model = HubUser
    hub_user_context_name = 'hub_user'

    def get_user_model(self):
        return self.user_model

    def get_context_data(self, **kwargs):
        kwargs = super(HubUserMixin, self).get_context_data(**kwargs)
        kwargs.update(
            {self.hub_user_context_name: self.object,
             self.hub_context_name: self.object.hub})
        return kwargs

    def get_object(self):
        """ Returns the HubUser object based on the primary keys for both
        the hub and the hub user.
        """
        if hasattr(self, 'hub_user'):
            return self.hub_user
        hub_slug = self.kwargs.get('hub_slug', None)
        user_username = self.kwargs.get('user_username', None)
        self.hub_user = get_object_or_404(
            HubUser.objects.select_related(),
            user__username=user_username, hub__slug=hub_slug)
        return self.hub_user


class MembershipRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.hub = self.get_hub()
        if not self.hub.is_member(request.user) and not (
                request.user.is_superuser):
            return HttpResponseForbidden(_("Wrong hub"))
        return super(MembershipRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class AdminRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.hub = self.get_hub()
        if not self.hub.is_admin(request.user) and not (
                request.user.is_superuser):
            return HttpResponseForbidden(_("Sorry, admins only"))
        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class OwnerRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.hub = self.get_hub()
        if self.hub.owner.hub_user.user != request.user and not (
                request.user.is_superuser):
            return HttpResponseForbidden(_("You are not the hub owner"))
        return super(OwnerRequiredMixin, self).dispatch(
            request, *args, **kwargs)
