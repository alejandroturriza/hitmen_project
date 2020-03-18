from hitmen_project.settings import *

ALLOWED_HOSTS = ['*']
DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hitmen',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
    }
}
