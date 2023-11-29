from .base import *
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mecanomobile',
        'USER': 'mosito',
        'PASSWORD': '1000', # Coloca aquí la contraseña que hayas asignado a mosito
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'