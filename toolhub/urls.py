""" Default urlconf for toolhub """

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('base.urls')),
    url(r'', include('accounts.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
