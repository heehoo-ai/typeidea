# flake8: NOQA
from .base import *  # NOQA


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


"""
不加HOST和PORT，虽然可以访问数据库，但会导致页面刷新变慢
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}