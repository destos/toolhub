from class_based_auth_views.views import LoginView, LogoutView
# from django.core.urlresolvers import reverse
from django.conf.urls import url, patterns
# from django.views.generic import TemplateView
from accounts.forms import LoginForm

from accounts import views


urlpatterns = patterns(
    'account.views',
    url(r'^account/$', views.AccountView.as_view(), name="account"),
    # maybe change these with:
    # https://github.com/django/django/blob/master/django/contrib/auth/forms.py
    url(r'^login/$', LoginView.as_view(
        form_class=LoginForm, template_name='accounts/login.jinja'),
        name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$',
        views.RegistrationView.as_view(), name='register'),
    url(r'^user/(?P<slug>[-_\w]+)/$',
        views.UserDetailView.as_view(), name='user-detail')
)
