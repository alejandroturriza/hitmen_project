from hitmen_project.settings import *

ALLOWED_HOSTS = ['*']
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hitmen',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
    }
}
