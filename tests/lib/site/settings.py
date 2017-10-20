# -*- coding: utf-8 -*-

import os.path

SECRET_KEY = '4'

DEBUG = True
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'ckeditor',
    'modeltranslation',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'crispy_forms',
    'chloroform',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth'
            ]
        },
        'APP_DIRS': True,
    },
]
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'robot-{}.sqlite'.format(os.getpid())),
    }
}
if os.environ.get('ROBOT_REUSE_DB'):
    DATABASES['default']['name'] = os.path.join(BASE_DIR, 'robot.sqlite')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(threadName)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'robot': {
            'level': 'DEBUG',
            'class': 'lib.logger.RobotRelayHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['robot'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['robot'],
            'propagate': False,
        },
        'requests': {
            'level': 'WARNING',
            'propagate': True,
        }
    }
}

CHLOROFORM_DOMAIN = 'https://chloro.form'
CHLOROFORM_TARGET_EMAILS = ['admin@chloro.form']
ROOT_URLCONF = 'lib.site.urls'

USE_TZ = True
USE_I18N = True
