# https://docs.djangoproject.com/en/1.10/ref/settings/

import os
import stripe
import shippo

from decouple import config  # noqa


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def base_dir_join(*args):
    return os.path.join(BASE_DIR, *args)


SITE_ID = 1

SECURE_HSTS_PRELOAD = True

DEBUG = True

ADMINS = (("Admin", "admin@unboxxen.com"),)

AUTH_USER_MODEL = "users.User"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_js_reverse",
    'rest_framework',
    'rest_framework.authtoken',
    "webpack_loader",
    "import_export",
    "rest_auth",
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'django_tables2',
    "fcm_django",

    "authorize",
    "api",
    "common",
    "products",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

FCM_DJANGO_SETTINGS = {
        "APP_VERBOSE_NAME": "unboxxen",
        "FCM_SERVER_KEY": "AAAAEblAs1A:APA91bHr4W0i_1JmjBzL3-dOIbH9HtXv8oZOATEcYMi3oxUFa6m44k-yqpjyUoXO-R-veKa02ArCUHn4eszpQZ1tkrlNzCiDIhTcHHtmh6yDhWxl4xnFBpbNn6igmPwz3SDbGFe5-fnA",
        "ONE_DEVICE_PER_USER": True,
        "DELETE_INACTIVE_DEVICES": True,
}

ROOT_URLCONF = "unboxxen.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir_join("templates")],
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

WSGI_APPLICATION = "unboxxen.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (base_dir_join("./templates/assets"),)

# Webpack
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,  # on DEBUG should be False
        "STATS_FILE": base_dir_join("../webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [".+\.hot-update.js", ".+\.map"],
    }
}

# Celery
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACKS_LATE = True
CELERY_TIMEZONE = TIME_ZONE

# Sentry
SENTRY_DSN = config("SENTRY_DSN", default="")
COMMIT_SHA = config("HEROKU_SLUG_COMMIT", default="")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'api.serializers.LoginSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

stripe.api_key = config("STRIPE_API_KEY")
shippo.config.api_key = config("SHIPPO_API_KEY")
shippo.config.api_version = config("SHIPPO_API_VERSION")
