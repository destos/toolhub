from django.conf.urls import include, patterns, url

from . import views
from . import backends

# namespaced under hubs:
urlpatterns = patterns(
    '',
    # Hub URLs
    url(r'^$', view=views.HubList.as_view(),
        name="list"),
    url(r'^mine/$', view=views.UserHubList.as_view(),
        name="user_hub_list"),
    url(r'^add/$', view=views.HubCreate.as_view(),
        name="hubs:add"),
    url(r'^(?P<hub_slug>[-_\w]+)/$',
        view=views.HubDetail.as_view(),
        name="detail"),
    url(r'^(?P<hub_slug>[-_\w]+)/edit/$',
        view=views.HubUpdate.as_view(),
        name="edit"),
    url(r'^(?P<hub_slug>[-_\w]+)/delete/$',
        view=views.HubDelete.as_view(),
        name="delete"),

    # Hub user URLs
    url(r'^(?P<hub_slug>[-_\w]+)/members/$',
        view=views.HubUserList.as_view(),
        name="user_list"),
    url(r'^(?P<hub_slug>[-_\w]+)/members/add/$',
        view=views.HubUserCreate.as_view(),
        name="user_add"),
    url(r'^(?P<hub_slug>[-_\w]+)/members/(?P<user_username>[-_\w]+)/remind/$',
        view=views.HubUserRemind.as_view(),
        name="user_remind"),
    url(r'^(?P<hub_slug>[-_\w]+)/members/(?P<user_username>[-_\w]+)/$',
        view=views.HubUserDetail.as_view(),
        name="user_detail"),
    url(r'^(?P<hub_slug>[-_\w]+)/members/(?P<user_username>[-_\w]+)/edit/$',
        view=views.HubUserUpdate.as_view(),
        name="user_edit"),
    url(r'^(?P<hub_slug>[-_\w]+)/members/(?P<user_username>[-_\w]+)/delete/$',
        view=views.HubUserDelete.as_view(),
        name="user_delete"),
    url(r'^invite/', include(backends.InvitationBackend().get_urls())),
    url(r'^register/', include(backends.RegistrationBackend().get_urls())),
)
