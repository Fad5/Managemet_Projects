from pathlib import Path
import os

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]