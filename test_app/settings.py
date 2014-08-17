import os
current_path = os.path.abspath(os.path.curdir)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}
USE_TZ = True
SITE_ID = 1
SECRET_KEY = 'keepitsecretkeepitsafe'

ROOT_URLCONF = 'test_app.urls'
STATIC_URL = '/static/'
MEDIA_ROOT = '%s/files' % current_path

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'south',
    'django_extensions',
    'django_jinja',
    'mptt',
    'class_based_auth_views',
    'password_reset',
    'crispy_forms',
    'accounts',
    'base',
    'tools',
    'hubs',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ('--nocapture', )
SOUTH_TESTS_MIGRATE = False
CELERY_ALWAYS_EAGER = True

COMPRESS_ROOT = STATIC_URL
