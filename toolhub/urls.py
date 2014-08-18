""" Default urlconf for toolhub """

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django_nyt.urls import get_pattern as get_nyt_pattern
from django_jinja import views as jinja_views

from .views import Homepage


handler403 = jinja_views.PermissionDenied.as_view()
handler404 = jinja_views.PageNotFound.as_view()
handler500 = jinja_views.ServerError.as_view()

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
    url(r'^$', Homepage.as_view(), name='home'),
    url(r'^', include('waffle.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
