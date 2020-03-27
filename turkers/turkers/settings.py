"""
Django settings for turkers project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import dj_database_url
import django_heroku
import os
import sentry_sdk
from better_profanity import profanity
from decouple import config
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).parents[1]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRDY_PARTY_LIBS = [
    "django_extensions",
    "debug_toolbar",
    "django_registration",
    "naomi",
    "rest_framework",
    "rest_framework_swagger",
    "webpack_loader",
]

PROJ_APPS = [
    "users",
    "chats",
]

INSTALLED_APPS = DJANGO_APPS + THIRDY_PARTY_LIBS + PROJ_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "turkers.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "turkers.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:postgres@localhost:5432/turkers')
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "users.User"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # segundos * minutos * horas * dias
# sessão dura 1 mês

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"


EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend", cast=str
)
EMAIL_FILE_PATH = "/tmp"
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default='', cast=str).strip(),
}
DEFAULT_FROM_EMAIL = 'Exchanges w/Turkers <contact@withturkers.net>'
EMAIL_SUBJECT_PREFIX = '[Exchanges w/Turkers] '


ACCOUNT_ACTIVATION_DAYS = config("ACCOUNT_ACTIVATION_DAYS", default=15, cast=int)
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "chats:index"
LOGOUT_REDIRECT_URL = "chats:index"


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": ("turkers.authentication.SessionAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'new_messages': '12/minute',
        'default_scope': '100/second',
        # valor default alto para não forçar limite para além da escrita de novas mensagens
    }
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
    }
}


# reCaptcha
GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY', cast=str)


# Config sentry
SENTRY_DSN = config('SENTRY_DSN', cast=str, default='')
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    MIDDLEWARE.insert(0, 'django.middleware.security.SecurityMiddleware')


# Cache configuration
REDIS_URL = config('REDISCLOUD_URL', '')
CACHE_DEFAULT_TIMEOUT = 60 * 60 * 24  # 1 day

if REDIS_URL.startswith('redis'):
    CACHES = {
        "default": {
            "TIMEOUT": CACHE_DEFAULT_TIMEOUT,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "dj-cache-",
        }
    }
else:
    CACHES = {
        "default": {
            "TIMEOUT": CACHE_DEFAULT_TIMEOUT,
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": '/tmp/',
            "KEY_PREFIX": "dj-cache-"
        }
    }


# Load badwords list
words_list = Path(BASE_DIR, 'turkers', 'profanity_wordlist.txt')
assert words_list.exists()
with open(words_list) as fd:
    bad_words = [l.strip() for l in fd.readlines() if l.strip()]
    profanity.load_censor_words(bad_words)


# Configure Django App for Heroku.
django_heroku.settings(locals())
