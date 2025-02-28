"""
Django settings for django_react project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import bmemcached
import pickle
import environ
root = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

LOGIN_REDIRECT_URL = "dashboard"
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6)cij^8dszki@+-2zbke%9gbu09ced6$)=n)1_&#5%32x&leab'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'konaequity.pythonanywhere.com',
    'www.konaequity.com',
    '66.8.137.66',
    '127.0.0.1',
    'localhost',
    '*'
]


# Setings for background tasks
MAX_ATTEMPTS = 5

# Hubspot client secret
HUBSPOT_SECRET = "c5b7b957-36b0-4543-85fc-71c3cb2c22f0"

# IP geolocation configuration
IP_KEY = "9eb42555eec85339c57761427530ae47"
DEFAULT_STATE = "CA"
BLACKLIST = []

# Akismet Spam detection Config
AKISMET_API_KEY = "18d40966c896"
AKISMET_BLOG_URL = "https://www.konaequity.com"

# Application definition
INSTALLED_APPS = [
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend_django.apps.BackendDjangoConfig',
    'auth_app.apps.AuthAppConfig',
    'background_task',
    'django.contrib.sitemaps',
    'django_mysql',
    'debug_toolbar',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'backend_django_v2',
    'sekizai',
    'watson',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'watson.middleware.SearchContextMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #     'django.middleware.cache.UpdateCacheMiddleware',
    #     'django.middleware.common.CommonMiddleware',
    #     'django.middleware.cache.FetchFromCacheMiddleware',
]

# Wagtail
WAGTAIL_SITE_NAME = 'Kona Equity'

# Silk profiling
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_INTERCEPT_PERCENT = 5

# for about page
MAX_ACCORDION_RESULTS = 5

# number of pages before showing popup for signup again
POPUP_WAIT = 3

# Cache definition
# def get_cache():
#   try:
#     servers = os.environ['MEMCACHIER_SERVERS']
#     username = os.environ['MEMCACHIER_USERNAME']
#     password = os.environ['MEMCACHIER_PASSWORD']
#     return {
#       'default': {
#         'BACKEND': 'django_bmemcached.memcached.BMemcached',
#         'TIMEOUT': None,
#         'LOCATION': servers,
#         'OPTIONS': {
#             'username': username,
#             'password': password,
#             'compression': None,
#             'socket_timeout': bmemcached.client.constants.SOCKET_TIMEOUT,
#             'pickler': pickle.Pickler,
#             'unpickler': pickle.Unpickler,
#             'pickle_protocol': 0
#         }
#       }
#     }
#   except:
#     return {
#       'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#       }
#     }

# CACHES = get_cache()

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'konacache',
    }
}

# Cache expiration times
EXP_LAVA = 3600     # 1 hour
EXP_HOT = 21600     # 6 hours
EXP_WARM = 43200    # 12 hours
EXP_COLD = 86400    # 1 day
EXP_ICE = 259200   # 3 days

ROOT_URLCONF = 'django_react.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_react.wsgi.application'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Database
# Local DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django_query_profiler.django.db.backends.mysql',
#         'NAME': 'konyequitydb',
#         'USER': 'konyequity',
#         'PASSWORD': '12345678',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# Original DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Konaequity$kona',
        'USER': 'Konaequity',
        'PASSWORD': '1a2b3c4d',
        'HOST': 'Konaequity.mysql.pythonanywhere-services.com',
        'CONN_MAX_AGE': 120
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'konaequity',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT':'3306',
#         'CONN_MAX_AGE': 120
#     }
# }



DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# allauth
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_FORMS = {
    'signup': 'auth_app.forms.CustomSignupForm',
}

SITE_ID = 4

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 50
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 3600  # 1 day in seconds
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'dashboard'
ACCOUNT_LOGOUT_REDIRECT_URL = "/"


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = "/home/Konaequity/konaequity/static"
# STATIC_ROOT = "/home/john/Desktop/konaequity/django_react/static"

STATICFILES_DIRS = [MEDIA_ROOT]


MAILJET_USERNAME = '378da14a414e906502f342d5d3accf04'
MAINJET_PASSWORD = '2fe3332c9dbd2fc3e8fde59aa999fcab'
MAILJET_SMTP_SERVER = 'in-v3.mailjet.com'
MAILJET_SMTP_PORT = '587'
MAILJECT_FROM_EMAIL = 'joey@konaequity.com'

def show_toolbar(request):
    try:
        return request.user and request.user.username == "ijohnmaged"
    except:
        return False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}


STRIPE_SECRET_KEY = env.str("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PUBLISHABLE_KEY")
STRIPE_ENDPOINT_SECRET = env.str("STRIPE_ENDPOINT_SECRET")
STRIPE_PRICE = env.str("STRIPE_PRICE")

# Email Configurations
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# This will disable warnings
# DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

