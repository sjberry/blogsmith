from django.conf import settings
from django.utils.module_loading import import_string
import pytz


def localize(datetime):
    return pytz.utc.localize(datetime)


if hasattr(settings, 'BLOGSMITH_AUTHOR_TZ_FUNCTION'):
    localize = import_string(settings.BLOGSMITH_AUTHOR_TZ_FUNCTION)
