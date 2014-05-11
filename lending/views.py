from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from django.utils.translation import ugettext_lazy as _

from braces.views import (
    LoginRequiredMixin, PrefetchRelatedMixin, SelectRelatedMixin,
    UserPassesTestMixin)

from hubs.mixins import MembershipRequiredMixin as HubMembershipRequiredMixin
from hubs.models import Hub
from tools.models import UserTool
from . import forms
from . import models
from .utils import new_lending_action


# TODO, check if requested tool is publicly available or available in hub
# user is a part of
# TODO: check for tool currently being lent
# Also check they you currently aren't attempting to lend this same tool
# ( exsiting request transation that hasn't been approved)
class StartTransationView(
        LoginRequiredMixin,
        HubMembershipRequiredMixin,
        CreateView):
    template_name = 'lending/start_transaction.jinja'
    form_class = forms.TransactionForm
    model = models.Transaction

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        # Catch permission/issues with this transaction and
        # send appropriate response
        try:
            self.usertool = self.get_usertool()
            return super(
                StartTransationView, self).dispatch(request, *args, **kwargs)
        except PermissionDenied, e:
            return HttpResponseForbidden(str(e))

    def get_usertool(self):
        usertool = get_object_or_404(
            UserTool, id=self.kwargs.get('usertool_id', None))
        # Can't lend to yourself...
        if usertool.owner == self.request.user:
            raise PermissionDenied(_("You can't lend a tool to yourself,"
                                     " silly goose."))
        return usertool

    def get_hub(self):
        """Used by MembershipRequiredMixin to retrieve hub data.
        We're using it to also check tool availability inside the hub.

        Called after self.get_usertool() so self.usertool is available."""
        hub = get_object_or_404(Hub, slug=self.kwargs.get('hub_slug', None))
        # TODO: check that this tool is being shared in this hub
        if False:
            raise PermissionDenied(_("Tool isn't available in this Hub"))
        return hub

    # TODO: make this more dry
    def get_form_kwargs(self):
        kwargs = super(StartTransationView, self).get_form_kwargs()
        kwargs.update({
            'hub_slug': self.kwargs.get('hub_slug', None),
            'usertool_id': self.kwargs.get('usertool_id', None)
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StartTransationView, self).get_context_data(**kwargs)
        context['hub'] = self.hub
        context['usertool'] = self.usertool
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # user i$ asking for this tool
        self.object.lendee = self.request.user
        # hub the tool was requested in
        self.object.hub = self.hub
        # the user's tool that has been requested
        self.object.tool = self.usertool
        self.object.save()
        # initial request action
        new_lending_action(transaction=self.object)
        return super(StartTransationView, self).form_valid(form)


class TransactionProgressView(
        LoginRequiredMixin,
        SelectRelatedMixin,
        PrefetchRelatedMixin,
        UserPassesTestMixin,
        DetailView):
    """
    Shows Transaction details and related history, in the future
    private communication can also occur.
    """
    template_name = 'lending/transaction_progress.jinja'
    model = models.Transaction
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_id'
    select_related = ('hub', 'tool', 'lendee',)
    prefetch_related = ('history',)

    def test_func(self, user):
        """
        Test for UserPassesTestMixin.
        Only allow the lendee or lender to see the transaction progress view.
        """
        self.object = self.get_object()
        return (self.object.lender == user or self.object.lendee == user)
