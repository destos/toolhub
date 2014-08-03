from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin as BracesLoginRequiredMixin
from braces.views import *


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
