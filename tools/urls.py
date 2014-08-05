from django.conf.urls import url, patterns
# from mptt_urls import url_mptt

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

# namespaced under tools:
urlpatterns = patterns(
    '',
    url(r'^$', views.ToolList.as_view(), name='list'),
    url(r'^add/$', views.CreateUserTool.as_view(), name='create'),
    url(r'^add/type/$', views.SuggestTool.as_view(), name='suggest'),
    url(r'^(?P<tool_slug>[-_\w]+)/$',
        views.ToolDetailView.as_view(), name='detail'),
    url(r'^category/(?P<tool_class_slug>[-_\w]+)/$',
        views.ToolList.as_view(), name='list_class')
   # (?P<class_id>\d+)/$
)

# tool_list_patterns = patterns(
#     # capturing pattern, place new urls above this
#     url_mptt(r'^(?P<url>.*)',
#              settings=mptt_urls_tool_settings,
#              name='list_class')
# )
