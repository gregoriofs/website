"""
Django settings for coderodojochi project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url
import django_heroku
import raven
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
RECAPTCHA_REQUIRED_SCORE = os.environ.get('RECAPTCHA_REQUIRED_SCORE', 0.85)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', True) == 'True'
if SECURE_SSL_REDIRECT:
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
    SESSION_COOKIE_HTTPONLY = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
    CSRF_COOKIE_HTTPONLY = True
    # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
    # set this to 60 seconds first and then to 518400 once you prove the former works
    SECURE_HSTS_SECONDS = 518400
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', True) == 'True'
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', True) == 'True'
    # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
    SECURE_CONTENT_TYPE_NOSNIFF = os.environ.get('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', True) == 'True'
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
    SECURE_BROWSER_XSS_FILTER = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
    X_FRAME_OPTIONS = 'DENY'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',

    'django.contrib.sites',
    'django.contrib.redirects',

    # vendor

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    'bootstrap3',
    'django_cleanup',
    'anymail',
    'html5',
    'loginas',
    'paypal.standard.ipn',
    'stdimage',
    'import_export',
    'django_nose',
    'stripe',
    'meta',
    'captcha',

    # apps
    'accounts',
    'coderdojochi',
    'weallcode',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',

    'coderdojochi.middleware.HandleExceptionMiddleware',
]

ROOT_URLCONF = 'coderdojochi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'accounts/templates/'),
            os.path.join(BASE_DIR, 'weallcode/templates/'),
            os.path.join(BASE_DIR, 'coderdojochi/templates/'),
            os.path.join(BASE_DIR, 'coderdojochi/templates/dashboard/'),
            os.path.join(BASE_DIR, 'coderdojochi/emailtemplates/'),
            os.path.join(BASE_DIR, 'coderdojochi/mentors/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Project
                'coderdojochi.context_processors.main_config_processor',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'coderdojochi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1
SITE_NAME = os.environ.get('SITE_NAME')
SITE_URL = os.environ.get('SITE_URL')

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ['django.contrib.staticfiles']

if DEBUG:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = [
        os.path.join(PROJECT_ROOT, 'static'),
        os.path.join(BASE_DIR, 'accounts/static'),
        os.path.join(BASE_DIR, 'weallcode/static'),
    ]

    # Media files
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

else:
    # STORAGES
    # ------------------------------------------------------------------------------
    # https://django-storages.readthedocs.io/en/latest/#installation
    INSTALLED_APPS += ['storages']  # noqa F405

    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_AUTO_CREATE_BUCKET = True
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_QUERYSTRING_AUTH = False
    # DO NOT change these unless you know what you're doing.
    _AWS_EXPIRY = 60 * 60 * 24 * 7
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
    }

    # STATIC
    # ------------------------
    STATICFILES_STORAGE = 'coderdojochi.settings.StaticRootS3BotoStorage'
    STATIC_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/static/'

    # MEDIA
    # ------------------------------------------------------------------------------
    # region http://stackoverflow.com/questions/10390244/
    from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile  # noqa E402
    from django.contrib.staticfiles.storage import ManifestFilesMixin

    # ManifestFilesSafeMixin = lambda: ManifestFilesMixin(manifest_strict=False)

    # Taken from an issue in django-storages:
    # https://github.com/jschneier/django-storages/issues/382#issuecomment-377174808
    class CustomS3Storage(ManifestFilesMixin, S3Boto3Storage):
        def _save_content(self, obj, content, parameters):
            """
            We create a clone of the content file as when this is passed to boto3 it wrongly closes
            the file upon upload where as the storage backend expects it to still be open
            """
            # Seek our content back to the start
            content.seek(0, os.SEEK_SET)

            # Create a temporary file that will write to disk after a specified size
            content_autoclose = SpooledTemporaryFile()

            # Write our original content into our copy that will be closed by boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the content_autoclose instance
            super(CustomS3Storage, self)._save_content(obj, content_autoclose, parameters)

            # Cleanup if this is fixed upstream our duplicate should always close
            if not content_autoclose.closed:
                content_autoclose.close()

    def StaticRootS3BotoStorage(): return CustomS3Storage(location='static')

    def MediaRootS3BotoStorage(): return S3Boto3Storage(location='media', file_overwrite=False)

    DEFAULT_FILE_STORAGE = 'coderdojochi.settings.MediaRootS3BotoStorage'
    MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/media/'

    # endregion


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'coderdojochi.CDCUser'


# Stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_LIVE_MODE = os.environ.get('STRIPE_LIVE_MODE')
# Django Meta
META_SITE_PROTOCOL = os.environ.get('META_SITE_PROTOCOL', 'https')
META_SITE_DOMAIN = os.environ.get('META_SITE_DOMAIN', 'www.weallcode.org')
META_SITE_NAME = SITE_NAME
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = False
META_USE_TITLE_TAG = False
META_TWITTER_SITE = os.environ.get('META_TWITTER_SITE', '@weallcode')
META_FB_APPID = os.environ.get('META_SITE_DOMAIN', '1454178301519376')
DEFAULT_META_DESCRIPTION = os.environ.get(
    'DEFAULT_META_DESCRIPTION',
    (
        'We All Code is volunteer run nonprofit organization that teaches web, game, '
        'and app development to youth ages 7 to 17 free of charge.'
    )
)
DEFAULT_META_KEYWORDS = os.environ.get('DEFAULT_META_KEYWORDS', '')
DEFAULT_META_TITLE = os.environ.get('DEFAULT_META_TITLE', '')


# Paypal
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')
PAYPAL_BUSINESS_ID = os.environ.get('PAYPAL_BUSINESS_ID')
PAYPAL_TEST = os.environ.get('PAYPAL_TEST') == 'True'


# django allauth
LOGIN_REDIRECT_URL = '/account'
LOGIN_URL = '/account/login'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = 'coderdojochi.forms.SignupForm'
SOCIALACCOUNT_ADAPTER = 'coderdojochi.social_account_adapter.SocialAccountAdapter'


# Email
ANYMAIL = {
    'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY'),
}
EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')
SENDGRID_UNSUB_CLASSANNOUNCE = int(os.environ.get('SENDGRID_UNSUB_CLASSANNOUNCE'))


# Sentry
SENTRY_DSN = os.environ.get('SENTRY_DSN', False)
INSTALLED_APPS += ['raven.contrib.django.raven_compat']

if SENTRY_DSN:
    import logging

    MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    ] + MIDDLEWARE

    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'INFO',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


# Debug toolbar
if DEBUG:

    def custom_show_toolbar(request):
        return True

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        'TAG': 'div',
        'ENABLE_STACKTRACES': True,
    }


# Activate Django-Heroku.
django_heroku.settings(locals(), staticfiles=False)
