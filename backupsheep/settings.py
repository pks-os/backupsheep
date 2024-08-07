"""
Django settings for backupsheep project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import io
import json
import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import google.auth
from dotenv import load_dotenv
from dotenv import dotenv_values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if "BACKUPSHEEP_SECRETS" in os.environ:
    config = json.loads(os.environ.get("BACKUPSHEEP_SECRETS"))
else:
    config = {
        **dotenv_values(".env"),  # load shared development variables
        **os.environ,  # override loaded values with environment variables
    }

# # environ.Env.read_env(".env")
SECRET_KEY = config["DJANGO_SECRET_KEY"]
DEBUG = config["DJANGO_DEBUG"]
DJANGO_SERVER = config["DJANGO_SERVER"]
ALLOWED_HOSTS = [config["DJANGO_ALLOWED_HOSTS"]]
HTTPS_ENABLED = False
CSRF_TRUSTED_ORIGINS = [f"{config['APP_PROTOCOL']}{config['APP_DOMAIN']}"]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.humanize",
    "django_user_agents",
    "django_filters",
    "django_celery_results",
    "django_celery_beat",
    'apps',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "utils.middleware.TimezoneMiddleware",
    "utils.middleware.RedirectMiddleware",

]

ROOT_URLCONF = "backupsheep.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR + "/apps/console/_templates/",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": config["DJANGO_DEBUG"],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.tz",
                "django.template.context_processors.i18n",
                "utils.context_processors.timezone",
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "core_cache",
    }
}

WSGI_APPLICATION = "backupsheep.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.api.v1.utils.api_authentication.CsrfExemptSessionAuthentication",
        "apps.api.v1.utils.api_authentication.CustomTokenAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
MIGRATION_MODULES = {"apps": "apps._migrations"}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["DB_NAME"],
        "USER": config["DB_USER"],
        "PASSWORD": config["DB_PASSWORD"],
        "HOST": config["DB_HOST"],
        "PORT": config["DB_PORT"],
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR + "/static/"

STATICFILES_DIRS = (
    ("console", BASE_DIR + "/apps/console/_static/console"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# App Settings
APP_NAME = config["APP_NAME"]
APP_DOMAIN = config["APP_DOMAIN"]
APP_PROTOCOL = config["APP_PROTOCOL"]
APP_URL = f"{APP_PROTOCOL}{APP_DOMAIN}"

sentry_sdk.init(
    dsn=config["SENTRY_DSN"],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations=[
        DjangoIntegration(
            transaction_style='url',
            middleware_spans=True,
            signals_spans=False,
            cache_spans=False,
        ),
    ],
    environment=DJANGO_SERVER
)

HOME_URL = "/console"
LOGIN_URL = "/login"
API_PATH = "/api/"
CONSOLE_URL = "/console"

LOGIN_REQUIRED_IGNORE_PATHS = [
    r'/login',
    r'/reset',
    r'/django-admin/',
    r'/api/',
    r'/error/',
]

# POSTMARK - Email Service
POSTMARK_API_KEY = config["POSTMARK_API_KEY"]
POSTMARK_DOMAIN = config["POSTMARK_DOMAIN"]
POSTMARK_EMAIL = config["POSTMARK_EMAIL"]
POSTMARK_API_URL = config["POSTMARK_API_URL"]

# AWS SES - Email Service
SES_REGION_NAME = config["SES_REGION_NAME"]
SES_REGION_ENDPOINT = config["SES_REGION_ENDPOINT"]
SES_ACCESS_KEY_ID = config["SES_ACCESS_KEY_ID"]
SES_SECRET_ACCESS_KEY = config["SES_SECRET_ACCESS_KEY"]

# MAILGUN - Email Service
MAILGUN_DOMAIN = config["MAILGUN_DOMAIN"]
MAILGUN_EMAIL = config["MAILGUN_EMAIL"]
MAILGUN_API_KEY = config["MAILGUN_API_KEY"]
MAILGUN_API_URL = config["MAILGUN_API_URL"]

# Options are postmark, mailgun and ses
EMAIL_PROVIDER = config["EMAIL_PROVIDER"]

# Storage to be used for application logs etc. Tested with AWS S3 and Cloudflare R2
S3_ACCESS_KEY_ID = config["S3_ACCESS_KEY_ID"]
S3_SECRET_ACCESS_KEY = config["S3_SECRET_ACCESS_KEY"]
S3_STORAGE_BUCKET_NAME = config["S3_STORAGE_BUCKET_NAME"]
S3_ENDPOINT_URL = config["S3_ENDPOINT_URL"]
S3_SIGNATURE_VERSION = config["S3_SIGNATURE_VERSION"]

# Dropbox Storage - Create Dropbox App and add keys in .env file
# Learn more: https://www.dropbox.com/developers/reference/getting-started#app%20console
DROPBOX_APP_KEY = config["DROPBOX_APP_KEY"]
DROPBOX_APP_SECRET = config["DROPBOX_APP_SECRET"]


# OneDrive Storage
MS_CLIENT_ID = config["MS_CLIENT_ID"]
MS_OBJECT_ID = config["MS_OBJECT_ID"]
MS_TENANT_ID = config["MS_TENANT_ID"]
MS_APPLICATION_ID = config["MS_APPLICATION_ID"]
MS_CLIENT_SECRET_VALUE = config["MS_CLIENT_SECRET_VALUE"]
MS_CLIENT_SECRET_ID = config["MS_CLIENT_SECRET_ID"]
MS_OAUTH_ENDPOINT = config["MS_OAUTH_ENDPOINT"]
MS_OAUTH_TOKEN_URL = config["MS_OAUTH_TOKEN_URL"]
MS_REDIRECT_URL = config["MS_REDIRECT_URL"]
MS_RESPONSE_TYPE = config["MS_RESPONSE_TYPE"]
MS_SCOPE = config["MS_SCOPE"]
MS_GRAPH_ENDPOINT = config["MS_GRAPH_ENDPOINT"]

# GOOGLE Storage
GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]