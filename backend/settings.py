"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from os import getenv, path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', 'cafawsdfaagshgh1441!4tgbcxnjzhdfZH')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG', True)

ALLOWED_HOSTS = [getenv('ALLOWED_HOSTS', '*')]

SITE_DOMAIN = getenv('SITE_DOMAIN', default='127.0.0.1:8000')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_yaml',
    'rest_framework',
    'rest_framework_simplejwt',
    'phonenumber_field',
    'celery',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.custom_jwt_middleware.CustomJWTMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': getenv('DB_NAME', 'default'),
        'HOST': getenv('DB_HOST', '127.0.0.1'),
        'PORT': getenv('DB_PORT', '5432'),
        'USER': getenv('DB_USER', 'postgres'),
        'PASSWORD': getenv('DB_PASSWORD', 'postgres')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.'
                 'password_validation.NumericPasswordValidator'),
    },
]

AUTH_USER_MODEL = 'app.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.AllowAllUsersRemoteUserBackend']

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    'TOKEN_OBTAIN_SERIALIZER': 'app.serializers.ObtainTokenSerializer',

}
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework_yaml.parsers.YAMLParser',
    ],
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}


EMAIL_BACKEND = getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
    )


EMAIL_ADDRESS = getenv('EMAIL_ADDRESS','default@email.com')
EMAIL_HOST = getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = getenv('EMAIL_PORT', 25)
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', 'default')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', 'default')
EMAIL_USE_TLS = getenv('EMAIL_USE_TLS', True)

REDIS_HOST = getenv('REDIS_HOST', default='localhost')
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/1'
CELERY_TASK_ALWAYS_EAGER = getenv('CELERY_TASK_ALWAYS_EAGER',False)
