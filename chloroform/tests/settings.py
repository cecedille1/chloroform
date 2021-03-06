import os.path

SECRET_KEY = '4'

DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'crispy_forms',
    'chloroform',
    'import_export',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'APP_DIRS': True,
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CHLOROFORM_DOMAIN = 'https://chloroform.emencia.io'
CHLOROFORM_TARGET_EMAILS = ['admin@chloro.form']
ROOT_URLCONF = 'chloroform.tests.test_views'
CRISPY_FAIL_SILENTLY = False

USE_TZ = True
