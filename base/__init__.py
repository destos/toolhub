"""Application base, containing global templates."""

# Jinja filters and globals
from django.conf import settings
from base.templatetags.customfilters import crispy

settings.JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
settings.JINJA2_GLOBALS['crispy'] = crispy
