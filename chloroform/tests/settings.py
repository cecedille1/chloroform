SECRET_KEY = '4'

DEBUG = True
INSTALLED_APPS = [
    'crispy_forms',
    'chloroform',
    'import_export',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
ROOT_URLCONF = 'chloroform.urls'

USE_TZ = True
