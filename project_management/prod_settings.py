from pathlib import Path
import os

SECRET_KEY = 'ww1h-im5j@7!8vu-m5eky_@zoj49@@4!f%*w3vwp&)l+rb!iql'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '[::1]']

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'management',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]