from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
                                  DeleteView, FormView)

from .models import Hub
from .mixins import (
    HubMixin, HubUserMixin, MembershipRequiredMixin, AdminRequiredMixin,
    OwnerRequiredMixin)
from .forms import (
    HubForm, HubUserForm, HubUserAddForm, HubAddForm, SignUpForm)
from .utils import create_hub
from .backends import InvitationBackend, RegistrationBackend
from lending.models import Transaction
from toolhub.mixins import LoginRequiredMixin


class BaseHubList(ListView):
    queryset = Hub.public.all()
    context_object_name = "hubs"
    template_name = 'hubs/hub_list.jinja'


class BaseHubDetail(HubMixin, DetailView):
    template_name = 'hubs/hub_detail.jinja'

    def get_context_data(self, **kwargs):
        context = super(BaseHubDetail, self).get_context_data(**kwargs)
        context['hub_users'] = self.hub.hub_users.all()
        context['hub'] = self.hub
        return context


class BaseHubCreate(CreateView):
    model = Hub
    form_class = HubAddForm
    template_name = 'hubs/hub_form.jinja'

    def get_success_url(self):
        return reverse("hub_list")

    def get_form_kwargs(self):
        kwargs = super(BaseHubCreate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseHubUpdate(HubMixin, UpdateView):
    form_class = HubForm
    template_name = 'hubs/hub_form.jinja'

    def get_form_kwargs(self):
        kwargs = super(BaseHubUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseHubDelete(HubMixin, DeleteView):
    template_name = 'hubs/hub_confirm_form.jinja'

    def get_success_url(self):
        return reverse("hub_list")


class BaseHubUserList(HubMixin, ListView):
    template_name = 'hubs/hubuser_list.jinja'

    def get(self, request, *args, **kwargs):
        self.hub = self.get_hub()
        self.object_list = self.hub.hub_users.all()
        context = self.get_context_data(
            object_list=self.object_list,
            hub_users=self.object_list,
            hub=self.hub)
        return self.render_to_response(context)


class BaseHubUserDetail(HubUserMixin, DetailView):
    template_name = 'hubs/hubuser_detail.jinja'

    def get_context_data(self, **kwargs):
        context = {
            'history': self.get_lending_history()
        }
        context.update(kwargs)
        return super(BaseHubUserDetail, self).get_context_data(**context)

    def get_lending_history(self):
        # filter by tool owner and lendee
        user = self.hub_user.user
        return Transaction.objects.filter(
            Q(tool__owner=user) | Q(lendee=user))


class BaseHubUserCreate(HubMixin, CreateView):
    form_class = HubUserAddForm
    template_name = 'hubs/hubuser_form.jinja'

    def get_success_url(self):
        return reverse('hub_user_list',
                       kwargs={'hub_slug': self.object.hub.slug})

    def get_form_kwargs(self):
        kwargs = super(BaseHubUserCreate, self).get_form_kwargs()
        kwargs.update({'hub': self.hub, 'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.hub = self.get_object()
        return super(BaseHubUserCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.hub = self.get_object()
        return super(BaseHubUserCreate, self).post(request, *args, **kwargs)


class BaseHubUserRemind(HubUserMixin, DetailView):
    template_name = 'hubs/hubuser_remind.jinja'
    # TODO move to invitations backend?

    def get_object(self, **kwargs):
        self.hub_user = super(BaseHubUserRemind, self).get_object()
        if self.hub_user.user.is_active:
            raise Http404(_("Already active"))  # TODO add better error
        return self.hub_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        InvitationBackend().send_reminder(
            self.object.user,
            **{'domain': get_current_site(self.request),
               'hub': self.hub, 'sender': request.user})
        return redirect(self.object)


class BaseHubUserUpdate(HubUserMixin, UpdateView):
    template_name = 'hubs/hubuser_form.jinja'
    form_class = HubUserForm


class BaseHubUserDelete(HubUserMixin, DeleteView):
    template_name = 'hubs/hubuser_confirm_delete.jinja'

    def get_success_url(self):
        return reverse('hub_user_list',
                       kwargs={'hub_slug': self.object.hub.slug})


class HubSignup(FormView):
    """
    View that allows unregistered users to create an hub account.

    It simply processes the form and then calls the specified registration
    backend.
    """
    form_class = SignUpForm
    template_name = "hubs/signup_form.jinja"
    # TODO get success from backend, because some backends may do something
    # else, like require verification
    backend = RegistrationBackend()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('hubs:add')
        return super(HubSignup, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if hasattr(self, 'success_url'):
            return self.success_url
        return reverse('hub_signup_success')

    def form_valid(self, form):
        """
        """
        user = self.backend.register_by_email(form.cleaned_data['email'])
        create_hub(
            user=user, name=form.cleaned_data['name'],
            slug=form.cleaned_data['slug'], is_active=False)
        return redirect(self.get_success_url())


# TODO: template view
def signup_success(self, request):
    return render(request, "hubs/signup_success.jinja", {})


class HubList(BaseHubList):
    pass


class UserHubList(LoginRequiredMixin, BaseHubList):
    """
    Show only enabled hubs that user is a member of
    """
    template_name = 'hubs/user_hub_list.jinja'

    def get_queryset(self):
        """
        get all enabled + allowing private hubs for the logged in user
        """
        user = self.request.user
        return super(
            UserHubList, self).get_queryset().enabled().get_for_user(user)


class HubCreate(LoginRequiredMixin, BaseHubCreate):
    """
    Allows any user to create a new hub.
    """
    pass


class HubDetail(LoginRequiredMixin, MembershipRequiredMixin, BaseHubDetail):
    pass


class HubUpdate(LoginRequiredMixin, AdminRequiredMixin, BaseHubUpdate):
    pass


class HubDelete(LoginRequiredMixin, OwnerRequiredMixin, BaseHubDelete):
    pass


class HubUserList(LoginRequiredMixin, MembershipRequiredMixin, BaseHubUserList):
    pass


class HubUserDetail(LoginRequiredMixin, AdminRequiredMixin, BaseHubUserDetail):
    pass


class HubUserUpdate(LoginRequiredMixin, AdminRequiredMixin, BaseHubUserUpdate):
    pass


class HubUserCreate(LoginRequiredMixin, AdminRequiredMixin, BaseHubUserCreate):
    pass


class HubUserRemind(LoginRequiredMixin, AdminRequiredMixin, BaseHubUserRemind):
    pass


class HubUserDelete(LoginRequiredMixin, AdminRequiredMixin, BaseHubUserDelete):
    pass


    pass
