import os

from . import base


## Email settings
SERVER_EMAIL = "tooly@toolhub.com"
DEFAULT_FROM_EMAIL = "tooly@toolhub.com"
SYSTEM_EMAIL_PREFIX = "[toolhub]"

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME", "")
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", "")
EMAIL_PORT = 25
EMAIL_USE_TLS = False

## Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MIDDLEWARE_CLASSES = base.MIDDLEWARE_CLASSES + [
    "sslify.middleware.SSLifyMiddleware"
]

## Log settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}


# Use Amazon S3 for storage for uploaded media files.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"

# Use Amazon S3 for static files storage.
STATICFILES_STORAGE = "require_s3.storage.OptimizedCachedStaticFilesStorage"

# Amazon S3 settings.
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False

# Cache settings.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    # Long cache timeout for staticfiles, since this is used heavily by the optimizing storage.
    "staticfiles": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 60 * 60 * 24 * 365,
        "LOCATION": "staticfiles",
    },
}
