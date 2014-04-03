""" Settings for toolhub """

from .base import *

try:
    env = get_env_setting('ENV')
except ImproperlyConfigured, exc:
    env = 'local'

try:
    exec "from .%s import *" % env
except ImportError, exc:
    exc.args = tuple(
        ['%s (error importing settings/%s.py)' % exc.args[0], env])
    raise exc
