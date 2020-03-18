from hitmen_project.settings import *
import os

ALLOWED_HOSTS = ['*']
DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}