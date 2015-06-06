from functools import wraps

from django.apps import AppConfig
from django.db.models.signals import pre_save


def autoconnect(cls):
    def connect(signal, func):
        @wraps(func)
        def wrapper(sender, instance, **kwargs):
            return func(instance)

        signal.connect(wrapper, sender=cls)

        return wrapper

    if hasattr(cls, 'pre_save'):
        cls.pre_save = connect(pre_save, cls.pre_save)

    return cls


class DefaultConfig(AppConfig):
    name = 'blogsmith'
    verbose_name = 'BlogSmith'

    def ready(self):
        for model in self.get_models():
            autoconnect(model)
