from django.conf.urls import url, patterns

from tools import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ToolList.as_view(), name='tool_list'),
    url(r'^(?P<tool_slug>[-_\w]+)/$',
        views.ToolDetailView.as_view(), name='tool_detail'),
    url(r'^category/(?P<tool_slug>[-_\w]+)/$',
        views.ToolDetailView.as_view(), name='tool_category_list')
)
