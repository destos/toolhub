from django.conf.urls import url, patterns, include
from mptt_urls import register as mptt_urls_register

from tools import views
from tools import models


mptt_urls_tool_settings = {
    'node': {
        'model': models.ToolClassification,
        'view': 'tools.views.ToolList',
        'parent': 'parent',
        'slug': 'slug',
    },
    'leaf': {
        'model': models.Tool,
        'view': 'tools.views.ToolDetailView',
        'parent': 'parent',
        'slug': 'slug',
    }
}

mptt_urls_register('tools', mptt_urls_tool_settings)

urlpatterns = patterns(
    '',
    url(r'^$', views.ToolList.as_view(), name='tool_list'),
    # url(r'^(?P<tool_slug>[-_\w]+)/$',
    #     views.ToolDetailView.as_view(), name='tool_detail'),
    # capturing pattern, place new urls above this
    url(r'^', include('mptt_urls.urls'), {
        'settings': mptt_urls_tool_settings}, name='tool_list_class'),

)
