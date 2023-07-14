"""
Django web app to manage and store drillhole data.
Copyright (C) 2023 Jorge Fuertes Blanco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Django settings for Deep Core project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO eliminar Secret key y Debug = False
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "192.168.1.150", "0.0.0.0"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'DH_app',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'DH_logger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = 'DH_logger.wsgi.application'

# Logging:
FORMATTERS = (
    {
    "verbose" : {
        "format": "{levelname} {asctime:s} {threadName} {thread:d}{module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
        "style" : "{",
    },
    "simple": {
        "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
        "style" : "{",
    },
    },
)
HANDLERS = {
    "console_handler": {
        "class" : "logging.StreamHandler",
        "formatter" :"simple",
    },
    "my_handler": {
        "class" : "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR,"logs","app_data.log"),
        "mode" : "a",
        "encoding" : "utf-8",
        "formatter" : "verbose",
        "backupCount" : 3,
        "maxBytes" : 1024*1024*3, # 3 MB
    },
    "detailed_handler" : {
        "class" : "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR,"logs","detailed_app_data.log"),
        "mode" : "a",
        "encoding" : "utf-8",
        "formatter" : "verbose",
        "backupCount" : 3,
        "maxBytes" : 1024*1024*3, # 3 MB
    },
}


LOGGERS = ({
    # INFO or higher
    "django": {
        "handlers": ["console_handler", "detailed_handler"],
        "level": "INFO",
        "propagate": False,
    },
    # WARNING or higher
    "django.request": {
        "handlers": ["my_handler"],
        "level": "WARNING",
        "propagate": False,
    },
},
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers" : False,
    "formatters" : FORMATTERS[0],
    "handlers" : HANDLERS,
    "loggers" : LOGGERS[0],
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'DH_db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [os.path.join(os.path.expanduser(BASE_DIR), "static")]
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(os.path.expanduser(BASE_DIR), "media")
MEDIA_URL = "/media/"

LOCALE_PATHS = (os.path.join(os.path.expanduser(BASE_DIR), "locale"),)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# File upload configuration
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB