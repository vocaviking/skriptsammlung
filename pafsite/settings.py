"""
Django settings for pafsite project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-5jb5px69h4#_l_-o9m*fl)-e44#fug67e!5a7dg1y2hgf$%5n'

#Recaptcha Plugin Keys
NORECAPTCHA_SITE_KEY   = '6LcMzAYTAAAAAM-sV5jFZFawm1Joo8Dpx4pKiUij'
NORECAPTCHA_SECRET_KEY = '6LcMzAYTAAAAAKy0ytmJ6uWGxpakCD6pJQDZQDQJ'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'series',
    'haystack',
    'reversion',
    'nocaptcha_recaptcha',
    'bootstrapform',
    'django.contrib.sites',
    'django_comments',
    'registration',
    'django.contrib.admin',
)

#Authentication Settings
REGISTRATION_OPEN       = True
ACCOUNT_ACTIVATION_DAYS = 3
INCLUDE_REGISTER_URL    = True
INCLUDE_AUTH_URLS       = True
LOGIN_URL               = '/users/login'
LOGIN_REDIRECT_URL      = 'series:index'
#LOGOUT_URL              = 'success'

#Needed for the comment system
SITE_ID = 1


# Allowed Upload File Types
SERIES_ALLOWED_MIMETYPES = (
    #These have Content Extraction
    'application/pdf',
    'text/plain',
    'application/x-tex',
    #These not
    #'image/jpeg',
)

# Maximums File Size in byte
SERIES_MAX_FILE_SIZE = 5242880

#where to save user uploads to
MEDIA_ROOT = 'uploads'

# Haystack Search Engine
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pafsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pafsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL  = '/static/'
STATIC_ROOT = './static/'