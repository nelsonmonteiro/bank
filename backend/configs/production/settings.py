from configs.common.settings import *

WSGI_APPLICATION = 'configs.production.wsgi.application'

DEBUG = False
ALLOWED_HOSTS = ['nelsonmonteiro.eu']
PROJECT_DOMAIN = 'https://nelsonmonteiro.eu'

try:
    from local_settings import *
except ImportError:
    pass
