from django.conf import settings
from django.utils.module_loading import import_string


def permission(view=None):
    return view


if hasattr(settings, 'BLOGSMITH_PERMISSION_FUNCTION'):
    permission = import_string(settings.BLOGSMITH_PERMISSION_FUNCTION)


class AuthenticationMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(AuthenticationMixin, cls).as_view(**kwargs)

        return permission(view)
