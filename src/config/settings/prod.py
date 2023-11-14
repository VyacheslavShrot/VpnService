from config.settings.base import *

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["localhost"]

STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'
