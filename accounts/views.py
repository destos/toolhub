from class_based_auth_views.views import (
    LoginView as ClassLoginView, LogoutView as ClassLogoutView)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from accounts.forms import RegisterForm, LoginForm


class LoginView(ClassLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.jinja'


class LogoutView(ClassLogoutView):
    template_name = 'accounts/logout.jinja'


# wanted to use CreateView, but that may not be the best use case
class RegistrationView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.jinja'
    # TODO: update
    # success_url = reverse('account')

    def form_valid(self, form):
        # create user and send validation messages
        form.save()
        return super(RegistrationView, self).form_valid(form)


class AccountView(DetailView):
    model = User


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.jinja'
    slug_field = 'username'
    model = User
    context_object_name = 'user'
