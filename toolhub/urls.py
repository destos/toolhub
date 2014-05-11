""" Default urlconf for toolhub """

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('accounts.urls', namespace='account')),
    url(r'^tools/', include('tools.urls', namespace='tools')),
    url(r'^hubs/', include('hubs.urls', namespace='hubs')),
    url(r'^lending/', include('lending.urls', namespace='lending')),
    url(r'', include('base.urls', namespace='base')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
