"""
Django settings for SIG_SMEHLA project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import load_config
from django.utils.translation import gettext_lazy as _


# configuration loader from config.ini file
config = load_config.ConfigLoader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.to_python(load_config.SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config.to_python(load_config.ALLOWED_HOSTS)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'services.apps.ServicesConfig',
    'news.apps.NewsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'SIG_SMEHLA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'SIG_SMEHLA.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = config.get_database_config()

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

TIME_ZONE = config.to_python(load_config.TIMEZONE)

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_URL = 'accounts:login'
INDEX_URL = 'services:index'

AUTH_USER_MODEL = 'accounts.Profile'

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
    ('pt', _('Portuguese')),
]

# DATE_INPUT_FORMATS = [
#     # '%m/%d/%Y', '%m/%d/%y'
#     '%Y/%m/%d'
# ]

# email configuration
EMAIL_HOST = config.to_python(load_config.EMAIL_HOST)
EMAIL_PORT = config.to_python(load_config.EMAIL_PORT)
EMAIL_HOST_USER = config.to_python(load_config.EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = config.to_python(load_config.EMAIL_HOST_PASSWORD)

# admin email
ADMINS = config.to_python(load_config.ADMINS)

# deployment configuration
# SECURE_HSTS_SECONDS = 3600  # 1 hours refuse to connect to your domain name via an insecure connection
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent the browser from identifying content types incorrectly
SECURE_BROWSER_XSS_FILTER = True  # Activate the browser's XSS filtering and help prevent XSS attacks
# SECURE_SSL_REDIRECT = True  # Redirect all connections to HTTPS
# SESSION_COOKIE_SECURE = True  # Makes it more difficult for network traffic sniffers to hijack user sessions
# CSRF_COOKIE_SECURE = True  # Makes it more difficult for network traffic sniffers to steal the CSRF token
X_FRAME_OPTIONS = 'DENY'  # unless there is a good reason for your site to serve other parts of itself in a frame
