from django.conf.urls import url, patterns
from accounts import views


urlpatterns = patterns(
    'account.views',
    url(r'^account/$', views.SettingsView.as_view(), name="account_settings"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^register/$', views.SignupView.as_view(), name='signup'),
    url(r'^user/(?P<username>[-_\w]+)/$',
        views.UserDetailView.as_view(), name='user_detail'),
    url(r"^confirm_email/(?P<key>\w+)/$", views.ConfirmEmailView.as_view(),
        name="account_confirm_email"),
    url(r"^password/$", views.ChangePasswordView.as_view(),
        name="account_password"),
    url(r"^password/reset/$", views.PasswordResetView.as_view(),
        name="account_password_reset"),
    url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$",
        views.PasswordResetTokenView.as_view(),
        name="account_password_reset_token"),
    url(r"^delete/$", views.DeleteView.as_view(), name="account_delete"),
)
