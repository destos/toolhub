from django.conf.urls import url, patterns
from mptt_urls import url_mptt

from tools import views


mptt_urls_tool_settings = {
    'node': {
        'model': 'tools.models.ToolClassification',
        'view': 'tools.views.ToolList',
        'slug_field': 'slug',
    },
    'leaf': {
        'model': 'tools.models.Tool',
        'view': 'tools.views.ToolDetailView',
        'slug_field': 'slug',
    }
}

urlpatterns = patterns(
    '',
    url(r'^$', views.ToolList.as_view(), name='tool_list'),
    # url(r'^(?P<tool_slug>[-_\w]+)/$',
    #     views.ToolDetailView.as_view(), name='tool_detail'),
    # capturing pattern, place new urls above this
    url_mptt(r'^(?P<url>.*)',
             settings=mptt_urls_tool_settings,
             name='tool_list_class'),

)
