import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from blogsmith.client import DropboxClient


default_app_config = 'blogsmith.apps.DefaultConfig'

if hasattr(settings, 'BLOGSMITH_OUTPUT_DIR'):
    ROOT_DIR = settings.BLOGSMITH_OUTPUT_DIR
elif settings.MEDIA_ROOT:
    ROOT_DIR = os.path.join(settings.MEDIA_ROOT, 'blogsmith')
else:
    raise ImproperlyConfigured('BlogSmith requires a "BLOGSMITH_OUTPUT_DIR" setting or a "MEDIA_ROOT" setting.')

if hasattr(settings, 'BLOGSMITH_DROPBOX_API_KEY'):
    DROPBOX_API_KEY = settings.BLOGSMITH_DROPBOX_API_KEY
    client = DropboxClient(DROPBOX_API_KEY)
else:
    raise ImproperlyConfigured('BlogSmith requires a Dropbox API key to sync files.')
