# -*- coding: utf-8 -*-
"""
Django settings for BasicPython project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
# If Debug=False, APACHE/NGINX would handle static files. In the meantime,
# local django cannot display static files well
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '192.168.1.101', '192.168.1.102', '127.0.0.1', '*']
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'Utility',
    'ipware',
    'blog',
    'blog.templatetags',
    'rest_framework',
    'Services',
    'uploader',

)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10,
    'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        )
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#HTML_MINIFY = True

ROOT_URLCONF = 'BasicPython.urls'

WSGI_APPLICATION = 'BasicPython.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASS = 'password'
MYSQL_DB   = 'BasicPython'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MYSQL_DB,                      # Or path to database file if using sqlite3.
        'USER': MYSQL_USER,                      # Not used with sqlite3.
        'PASSWORD': MYSQL_PASS,                  # Not used with sqlite3.
        'HOST': MYSQL_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': MYSQL_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

DEFAULT_CHARSET = 'UTF-8'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'static',
    os.path.join(BASE_DIR,  'static'),
    os.path.join(BASE_DIR,  'media'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

#ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"


# Global settings for values
MAIN_LIST_COUNT_PER_PAGE = 5    #Count for per page
MAIN_LIST_TRUNCATECHARS = 350
FILTER_TAG_TRUNCATECHARS = 300
FILTER_CATEGORY_TRUNCATECHARS = 300
SEARCH_TRUNCATECHARS = 100  #Return search out chars
DOMAIN_ADDRESS = "http://web.basicpython.com:9000"


# you can provide your own meta precedence order by
# including IPWARE_META_PRECEDENCE_ORDER in your
# settings.py. The check is done from top to bottom
IPWARE_META_PRECEDENCE_LIST = (
    'HTTP_X_FORWARDED_FOR', # client, proxy1, proxy2
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)

# you can provide your own private IP prefixes by
# including IPWARE_PRIVATE_IP_PREFIX in your setting.py
# IPs that start with items listed below are ignored
# and are not considered a `real` IP address
IPWARE_PRIVATE_IP_PREFIX = (
    '0.', '1.', '2.', # externally non-routable
    '10.', # class A private block
    '169.254.', # link-local block
    '172.16.', '172.17.', '172.18.', '172.19.',
    '172.20.', '172.21.', '172.22.', '172.23.',
    '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.', # class B private blocks
    '192.0.2.', # reserved for documentation and example code
    '192.168.', # class C private block
    '255.255.255.', # IPv4 broadcast address
) + (  # the following addresses MUST be in lowercase)
    '2001:db8:', # reserved for documentation and example code
    'fc00:', # IPv6 private block
    'fe80:', # link-local unicast
    'ff00:', # IPv6 multicast
)


# redis
CACHES = {
   "default": {
       "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# uploader
# When deployment, there would be some settings in NGINX BasicPython.conf
# MEDIA_ROOT should be different from local to production
MEDIA_ROOT = '/home/will/Documents/PycharmProjects/BasicPython/media/'
MEDIA_URL = '/media/'


# Email

#EMAIL_HOST = 'smtp.163.com'
#EMAIL_PORT = 25
#EMAIL_HOST_USER = 'xxxx@163.com'
#EMAIL_HOST_PASSWORD = 'xxxxx'
#EMAIL_SUBJECT_PREFIX = u'[BasicPython]'
#EMAIL_USE_TLS = True
#SERVER_EMAIL = 'xxxx@163.com'

BLOG_ROOT_URL = 'http://127.0.0.1:9000/blog/'
