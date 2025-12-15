from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Allow CSRF verification to pass for any local network address
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
