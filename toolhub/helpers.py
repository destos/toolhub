"""Template helpers loaded by Jingo to be used globally"""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Template, Context
from django.template.defaultfilters import date
from django.utils import timezone
import jinja2
from jingo import register


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.function
def now(format_string):
    return date(timezone.now(), format_string)


@register.function
@jinja2.contextfunction
def crispy(context, form, helper=None, template_pack='bootstrap'):
    mini_template = (
        '{%% load crispy_forms_tags %%}{%% crispy form "%s" %%}' %
        template_pack)
    t = Template(mini_template)
    context = Context(dict(context))
    context.update({'form': form})
    return t.render(context)
