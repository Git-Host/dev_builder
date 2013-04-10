import os
from django.conf import settings

SITE_PATH = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(SITE_PATH, "media")

MEDIA_URL = os.path.relpath(MEDIA_ROOT, settings.PROJECT_ROOT)
MEDIA_URL = os.sep + os.path.normpath(MEDIA_URL) + os.sep

# Set this so that when we run collectstatic,
# user edited files will get pulled in.
STATICFILES_DIRS = (
    os.path.join(SITE_PATH, "static") 
)