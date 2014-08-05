"""Application base, containing global templates."""

# Jinja filters and globals
from django.conf import settings
from .templatetags.customfilters import crispy, now

settings.JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
settings.JINJA2_GLOBALS['crispy'] = crispy
settings.JINJA2_GLOBALS['now'] = now
