from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from accounts.forms import RegisterForm


# wanted to use CreateView, but that may not be the best use case
class RegistrationView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.jinja'
    success_url = '/activate'  # reverse('accounts_activate')

    def form_valid(self, form):
        # create user and send validation messages
        form.save()
        return super(RegistrationView, self).form_valid(form)


class AccountView(DetailView):
    model = User


class UserDetailView(DetailView):
    model = User
