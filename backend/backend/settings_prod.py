from .settings import *

import pymysql

pymysql.install_as_MySQLdb()

DEBUG = True
LOCAL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ark2020',
        'USER': 'root',
        'PASSWORD': 'Joe!',
    }
}


STATIC_ROOT = '/var/ark2020/static/'
MEDIA_ROOT = '/var/ark2020/media/'