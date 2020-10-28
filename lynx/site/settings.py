"""
Django settings for lynx site.

"""

import logging.config
import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """Get the environment variable or return exception."""

    if default is None:
        try:
            return os.environ[var_name]
        except KeyError as err:
            error_msg = "Set the {} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg) from err
    else:
        return os.environ.get(var_name, default)


def get_env_boolean(var_name, default=None):
    value = get_env_variable(var_name, default)
    if isinstance(value, str) and value.lower() in ["false", "0"]:
        return False
    else:
        return bool(value)


def get_env_list(var_name, default=None, delimiter=","):
    values = get_env_variable(var_name, default).split(delimiter)
    return [value.strip() for value in values]


ENV = get_env_variable("ENV").lower()

if ENV not in ("dev", "prod", "staging", "test"):
    raise ImproperlyConfigured("Unknown environment for settings: " + ENV)

DEBUG = get_env_boolean("DEBUG")

if ENV == "prod" and DEBUG:
    raise ImproperlyConfigured("DEBUG = True is not allowed in production")


# #########
#   PATHS
# #########

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if ENV != "dev":
    MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
    STATIC_ROOT = os.path.join(ROOT_DIR, "static")

# #####################
#   APPS & MIDDLEWARE
# #####################

# The order of the apps is important when searching for templates. Allauth
# extends "base.html" so the demo app must come before allauth.account so
# the login and logout forms are displayed with the correct template.

INSTALLED_APPS = [
    "lynx.core.apps.LynxConfig",
    "lynx.site.apps.LynxConfig",
    "lynx.news.apps.LynxConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]


# ##############
#   WEB SERVER
# ##############

ROOT_URLCONF = "lynx.site.urls"

WSGI_APPLICATION = "lynx.site.wsgi.application"


# ############
#   DATABASE
# ############

if ENV == "dev":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": get_env_variable("DB_NAME"),
            "USER": get_env_variable("DB_USER"),
            "PASSWORD": get_env_variable("DB_PASSWORD"),
            "HOST": get_env_variable("DB_HOST"),
            "PORT": get_env_variable("DB_PORT"),
        }
    }

# ###########
#   CACHING
# ###########

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "site",
    }
}


# ############
#   SECURITY
# ############

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = get_env_list("ALLOWED_HOSTS")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# #############
#   TEMPLATES
# #############

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(ROOT_DIR, "templates")],
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

# ########################
#   INTERNATIONALIZATION
# ########################

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ################
#   STATIC FILES
# ################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# ###########
#   LOGGING
# ###########

# Based on the configuration in Peter Baumgartner's excellent article on
# logging, see https://lincolnloop.com/blog/django-logging-right-way/

LOGGING_CONFIG = None

LOGLEVEL = get_env_variable("LOGLEVEL", "INFO").upper()

DICT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "console": {
            "format": "[%(asctime)s|%(levelname)s|%(name)s.%(funcName)s|%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
        },
        "django": {
            "level": "INFO",
            "propagate": True,
        },
        "lynx": {
            "level": LOGLEVEL,
            "propagate": True,
        },
    },
}

SENTRY_DSN = get_env_variable("SENTRY_DSN", "")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(SENTRY_DSN, integrations=[DjangoIntegration(), CeleryIntegration()])

logging.config.dictConfig(DICT_CONFIG)


# #########
#   EMAIL
# #########

if ENV == "prod":
    EMAIL_HOST = get_env_variable("EMAIL_HOST")
    EMAIL_PORT = get_env_variable("EMAIL_PORT")
    EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = get_env_boolean("EMAIL_USE_TLS")
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(ROOT_DIR, "mail.log")

DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL", "noreply@lynx.com")


# ########
#   SITE
# ########

SITE_ID = 1


# ###########
#   ALLAUTH
# ###########

# The default is /accounts/login but allauth redirects to /account/login/
LOGIN_URL = "/account/login"

LOGIN_REDIRECT_URL = "/news"
LOGOUT_REDIRECT_URL = "/news"
