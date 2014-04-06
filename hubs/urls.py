from django.conf.urls import include, patterns, url
from django.contrib.auth.decorators import login_required

from . import views
from . import backends

urlpatterns = patterns(
    '',
    # Hub URLs
    url(r'^$', view=views.HubList.as_view(),
        name="hub_list"),
    url(r'^mine/$', view=login_required(views.UserHubList.as_view()),
        name="user_hub_list"),
    url(r'^add/$', view=login_required(views.HubCreate.as_view()),
        name="hub_add"),
    url(r'^(?P<hub_slug>[-_\w]+)/$',
        view=login_required(views.HubDetail.as_view()),
        name="hub_detail"),
    url(r'^(?P<hub_slug>[-_\w]+)/edit/$',
        view=login_required(views.HubUpdate.as_view()),
        name="hub_edit"),
    url(r'^(?P<hub_slug>[-_\w]+)/delete/$',
        view=login_required(views.HubDelete.as_view()),
        name="hub_delete"),

    # Hub user URLs
    url(r'^(?P<hub_slug>[-_\w]+)/people/$',
        view=login_required(views.HubUserList.as_view()),
        name="hub_user_list"),
    url(r'^(?P<hub_slug>[-_\w]+)/people/add/$',
        view=login_required(views.HubUserCreate.as_view()),
        name="hub_user_add"),
    url(r'^(?P<hub_slug>[-_\w]+)/people/(?P<user_username>[-_\w]+)/remind/$',
        view=login_required(views.HubUserRemind.as_view()),
        name="hub_user_remind"),
    url(r'^(?P<hub_slug>[-_\w]+)/people/(?P<user_username>[-_\w]+)/$',
        view=login_required(views.HubUserDetail.as_view()),
        name="hub_user_detail"),
    url(r'^(?P<hub_slug>[-_\w]+)/people/(?P<user_username>[-_\w]+)/edit/$',
        view=login_required(views.HubUserUpdate.as_view()),
        name="hub_user_edit"),
    url(r'^(?P<hub_slug>[-_\w]+)/people/(?P<user_username>[-_\w]+)/delete/$',
        view=login_required(views.HubUserDelete.as_view()),
        name="hub_user_delete"),
    url(r'^invite/', include(backends.InvitationBackend().get_urls())),
    url(r'^register/', include(backends.RegistrationBackend().get_urls())),
)
