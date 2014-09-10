""" Default urlconf for toolhub """

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django_nyt.urls import get_pattern as get_nyt_pattern

from . import views


handler403 = views.PermissionDenied.as_view()
handler400 = views.BadRequest.as_view()
handler404 = views.PageNotFound.as_view()
handler500 = views.ServerError.as_view()

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('accounts.urls', namespace='account')),
    url(r'^tools/', include('tools.urls', namespace='tools')),
    url(r'^hubs/', include('hubs.urls', namespace='hubs')),
    url(r'^lending/', include('lending.urls', namespace='lending')),
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^$', views.Homepage.as_view(), name='home'),
    url(r'^', include('waffle.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^404/', views.PageNotFound.as_view(), name='404'),
        url(r'^400/', views.BadRequest.as_view(), name='400'),
        url(r'^403/', views.PermissionDenied.as_view(), name='403'),
        url(r'^500/', views.ServerError.as_view(), name='500'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
