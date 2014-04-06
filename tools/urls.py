from django.conf.urls import url, patterns

from tools import views

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-_\w]+)/$',
        views.ToolDetailView.as_view(), name='tool-detail'),
    url(r'^category/(?P<slug>[-_\w]+)/$',
        views.ToolDetailView.as_view(), name='tool-category-list')
)
