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

ALLOWED_HOSTS = ['127.0.0.1','192.168.3.103','10.192.12.148']
STATIC_ROOT = '/var/ark2020/static/'
MEDIA_ROOT = '/var/ark2020/media/'
