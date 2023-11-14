from config.settings.base import *

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []

STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'
