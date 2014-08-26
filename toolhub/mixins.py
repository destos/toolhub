from braces.views import *
from braces.views import LoginRequiredMixin as BracesLoginRequiredMixin
from braces.views._access import AccessMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
import waffle


# abstract the object retrieval?
class MPTTUrlMixin(object):
    mptt_context_object_name = 'mptt_object'

    def dispatch(self, request, *args, **kwargs):
        """get passed in mptt_urls object which is the leaf node"""
        self.mptt_object = kwargs.pop('mptt_urls', {}).get('object', None)
        return super(MPTTUrlMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, object=None):
        context = super(MPTTUrlMixin, self).get_context_data()
        context[self.mptt_context_object_name] = self.mptt_object
        return context


class LoginRequiredMixin(BracesLoginRequiredMixin):
    login_url = reverse_lazy("account:login")
    redirect_field_name = "return"


class WaffleRequired(AccessMixin):
    raise_exception = True

    waffle_flags = []
    waffle_switches = []
    waffle_samples = []

    def perform_redirect(self, request):
        return redirect_to_login(request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())

    def dispatch(self, request, *args, **kwargs):
        for flag in self.waffle_flags:
            if not waffle.flag_is_active(request, flag):
                if self.raise_exception:
                    raise PermissionDenied
                else:
                    return self.perform_redirect(request)
        for switch in self.waffle_switches:
            if not waffle.switch_is_active(switch):
                if self.raise_exception:
                    raise PermissionDenied
                else:
                    return self.perform_redirect(request)
        for sample in self.waffle_samples:
            if not waffle.sample_is_active(sample):
                if self.raise_exception:
                    raise PermissionDenied
                else:
                    return self.perform_redirect(request)

        return super(WaffleRequired, self).dispatch(
            request, *args, **kwargs)


class RestrictToUserMixin(LoginRequiredMixin):
    """
    Extends braces.views.LoginRequiredMixin

    View mixin for SingleObjectMixin views that restricts the
    queryset to only objects related to the request user.

    specify the model foreign key field with property: restrict_user_field
    """
    restrict_user_field = 'user'

    def get_queryset(self):
        self.queryset = super(
            RestrictToUserMixin, self).get_queryset().filter(**{
                self.restrict_user_field: self.request.user})
        return self.queryset
