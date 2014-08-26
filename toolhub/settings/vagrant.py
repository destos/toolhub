# flake8: noqa
from .local_dist import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "toolhub_db",
        "USER": "toolhub_user",
        "PASSWORD": "CWMFgG89RBnPGbWUPogFrMk",
        "HOST": "localhost",
        "PORT": "",
    }
}
