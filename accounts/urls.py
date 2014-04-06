# from django.core.urlresolvers import reverse
from django.conf.urls import url, patterns
# from django.views.generic import TemplateView

from accounts import views


urlpatterns = patterns(
    'account.views',
    url(r'^account/$', views.AccountView.as_view(), name="account"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^user/(?P<slug>[-_\w]+)/$',
        views.UserDetailView.as_view(), name='user-detail')
)
