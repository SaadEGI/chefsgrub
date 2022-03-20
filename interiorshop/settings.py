"""
Django settings for interiorshop project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import environ
import os
import dj_database_url



env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent


PRODUCTION = os.environ.get('DATABASE_URL') != None
ENVIRONMENT = os.environ.get('ENVIRONMENT')
# SECRET_KEY = 'wmmx*^_i6@p)kP5nxa=89byfm0=gzc_h%13q)*7g7+181rk0po' # TODO: get from os.environ.get('SECRET_KEY), inject it in pipeline
if(ENVIRONMENT == 'staging' or ENVIRONMENT == 'production'):
    SECRET_KEY = os.environ.get("SECRET_KEY")
else:
    SECRET_KEY = 'tuxik&w(xnck86#t!asbp67u$##glq!#08y35%2kxrt!-3i%0n'
# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
if(ENVIRONMENT == 'production' or ENVIRONMENT == 'staging'):
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

STRIPE_PUB_KEY = 'pk_test_51HIHiuKBJV2qfWbD2gQe6aqanfw6Eyul5P02KeOuSR1UMuaV4TxEtaQyzr9DbLITSZweL7XjK3p74swcGYrE2qEX00Hz7GmhMI'
STRIPE_SECRET_KEY = 'sk_test_51HIHiuKBJV2qfWbD4I9pAODack7r7r9LJOY65zSFx7jUUwgy2nfKEgQGvorv1p2xP7tgMsJ5N9EW7K1lBdPnFnyK00kdrS27cj'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'vendor_admin' # TODO: change to accomodate chef
LOGOUT_REDIRECT_URL = 'frontpage'

SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_EMAIL_FROM = 'Interiorstore <noreply@codewithstein.com>'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.cart',
    'apps.core',
    'apps.order',
    'apps.product',
    'apps.vendor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interiorshop.urls'

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
                'apps.product.context_processors.menu_categories',
                'apps.cart.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'interiorshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CHEFSGRUB', 
        'USER': 'strtpadmin', 
        'PASSWORD': 'strtpadmin',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}
if PRODUCTION:# or ENVIRONMENT == 'staging':
    DATABASES['default'] = dj_database_url.config()


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/' # TODO Probably not needed. In that case, it should be deleted
STATICFILES_DIRS = [
    (BASE_DIR / 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'