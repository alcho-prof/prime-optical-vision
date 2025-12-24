"""
Production settings for Prime Optical Vision.

This file contains production-specific settings including:
- MySQL database configuration
- Security settings
- Static/Media file handling
- Email configuration
"""

from .base import *
import os

# SECURITY SETTINGS
DEBUG = True  # Set to False in actual production

# Add your production domain here
ALLOWED_HOSTS = [
    'primeoptical.in',
    'www.primeoptical.in',
    'localhost',
    '127.0.0.1',  # For local testing
]

# Security Headers (Disabled for local testing, enable in actual production)
SECURE_SSL_REDIRECT = False  # Set to True in actual production
SESSION_COOKIE_SECURE = False  # Set to True in actual production
CSRF_COOKIE_SECURE = False  # Set to True in actual production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 0  # Set to 31536000 in actual production
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Set to True in actual production
SECURE_HSTS_PRELOAD = False  # Set to True in actual production

# MySQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'prime_optical_db'),
        'USER': os.environ.get('DB_USER', 'prime_optical_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Email Configuration (Update with your SMTP settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@primeoptical.in')

# Static Files (Production)
# Whitenoise will serve static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files (Production)
# Consider using cloud storage (AWS S3, Google Cloud Storage) for production
MEDIA_ROOT = BASE_DIR / 'media'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache Configuration (Optional - Redis recommended for production)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
#     }
# }
