"""Application base, containing global templates."""

# Jinja filters and globals
from django.conf import settings
from waffle import flag_is_active, sample_is_active, switch_is_active
from waffle.views import _generate_waffle_js
import jinja2

from .templatetags.customfilters import crispy, now


settings.JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
settings.JINJA2_GLOBALS['crispy'] = crispy
settings.JINJA2_GLOBALS['now'] = now


@jinja2.contextfunction
def flag_helper(context, flag_name):
    return flag_is_active(context['request'], flag_name)


@jinja2.contextfunction
def inline_wafflejs_helper(context):
    return _generate_waffle_js(context['request'])


settings.JINJA2_GLOBALS['waffle'] = {
    'flag': flag_helper,
    'switch': switch_is_active,
    'sample': sample_is_active,
    'wafflejs': inline_wafflejs_helper
}
