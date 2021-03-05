from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '54.169.85.93']

STATIC_ROOT = os.path.join(BASE_DIR, '..', '..', 'public', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', '..', 'public', 'media')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '829003938200-ho1ot0uggcvpdcm6sj11qspvg8v418at.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'NOEVLvmvyA2qprq8o6bcDzud'
# You can owerwrite it in your local.py file
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'TOF',
#         'USER': 'ubuntu',
#         'PASSWORD': '',
#         'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'),
#         'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
try:
    from .local import *
except ImportError:
    pass
