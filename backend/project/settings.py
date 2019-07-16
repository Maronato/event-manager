"""Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# logging.basicConfig(level=logging.DEBUG)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Website root url
ROOT_URL = os.environ.get('ROOT_URL', 'localhost:8000')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'abc123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get('DEBUG', 'False').capitalize())
SHOW_TOOLBAR_CALLBACK = eval(os.environ.get("SHOW_TOOLBAR_CALLBACK", "DEBUG"))
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda r: (
        SHOW_TOOLBAR_CALLBACK and r.user.is_superuser
    )  # disables it
}

ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS', '["*"]'))

if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()]
    )

# Application definition

INSTALLED_APPS = [
    'scout_apm.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maintenance_mode',

    'storages',
    'djcelery_email',
    'django_prometheus',
    'django_celery_beat',

    'rest_framework',
    'corsheaders',

    "debug_toolbar",
    'django_extensions',

    'channels',
    'model_sockets',

    'dashboard',
    'user_profile',
    'social',
    'hacker',
    'staff',
    'settings',
    'application',
    'godmode',
    'company',
    'announcement',
    'stats',
    'schedule',
    'helper',
    'team',

    'pagseguro',
]


MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.event_info'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django_prometheus.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_SERVER')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

if os.environ.get('REDIS_URL'):
    # Cache backend
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": "djangocache"
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Project urls
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'http://localhost:3000/'

# AWS Storage settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

if not DEBUG and AWS_STORAGE_BUCKET_NAME:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_MAX_AGE = 60 * 60


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


if not DEBUG and eval(os.environ.get("USE_SSL", "False")):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Celery stuff
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = eval(os.environ.get('EMAIL_USE_TLS', 'True'))
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
DEFAULT_CONTACT_EMAIL = os.environ.get('DEFAULT_CONTACT_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', EMAIL_HOST_USER)
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

ADMINS = [('Admin', os.environ.get('ADMIN_ACCOUNT')), ]


# Event data
EVENT_NAME = os.environ.get('EVENT_NAME', 'Meu evento')
EVENT_DESCRIPTION = os.environ.get('EVENT_DESCRIPTION', '')
TOKEN_SIZE = eval(os.environ.get('TOKEN_SIZE', '5'))


# Model Sockets settings
# Name of the app containing the self model
MSOCKS_SELF_APP = 'user_profile'
# Name of the self Model
MSOCKS_SELF_MODEL = 'Profile'
MSOCK_AUTH_USER_RELATION_ID = 'user.profile.id'
MSOCKS_SELF_SUBSCRIPTION_SERIALIZER = 'user_profile.serializers.SelfSubscriptionSerializer'

# Override model sockets router
ASGI_APPLICATION = "project.router_application.application"

SHOW_TOOLBAR_CALLBACK = eval(str(os.environ.get('SHOW_TOOLBAR_CALLBACK', DEBUG)).capitalize())

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: SHOW_TOOLBAR_CALLBACK and r.user.is_superuser  # disables it
    # '...
}

# Maintenance mode
MAINTENANCE_MODE = eval(os.environ.get('MAINTENANCE_MODE', 'False').capitalize())
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_SUPERUSER = True

# Scout Monitor
SCOUT_NAME = EVENT_NAME


# PagSeguro settings
PAGSEGURO_EMAIL = os.environ.get('PAGSEGURO_EMAIL', '')
PAGSEGURO_TOKEN = os.environ.get('PAGSEGURO_TOKEN', '')
PAGSEGURO_SANDBOX = eval(os.environ.get('PAGSEGURO_SANDBOX', str(DEBUG)).capitalize())
PAGSEGURO_LOG_IN_MODEL = True

# Django Prometheus
PROMETHEUS_EXPORT_MIGRATIONS = False

# Shell plus settings
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS = "ptipython"
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(reindent_aligned=True, truncate_strings=1000)


# Rest Settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

JWT_AUTH = {
    "JWT_ALLOW_REFRESH": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=1),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_LEEWAY": 30,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
