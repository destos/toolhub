from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns(
    'base.views',
    url(r'^$', TemplateView.as_view(template_name="base/home.jinja"))
)
