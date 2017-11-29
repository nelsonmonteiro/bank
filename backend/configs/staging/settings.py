from configs.common.settings import *

WSGI_APPLICATION = 'configs.staging.wsgi.application'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

try:
    from local_settings import *
except ImportError:
    pass
