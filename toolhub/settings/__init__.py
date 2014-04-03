""" Settings for toolhub """

from .base import *

try:
    env = get_env_setting('ENV')
except ImproperlyConfigured:
    env = 'local'

try:
    exec "from .%s import *" % env
except ImportError, exc:
    # TODO: log error
    print '%s (error importing settings/%s.py)' % (exc.args[0], env)
    # exc.args = tuple(
    #     ['%s (error importing settings/%s.py)' % (exc.args[0], env)])
    # raise exc
