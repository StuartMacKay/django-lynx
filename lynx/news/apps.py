from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_app_settings():
    from django.conf import settings

    from . import settings as defaults

    for name in dir(defaults):
        if name.isupper() and not hasattr(settings, name):
            setattr(settings, name, getattr(defaults, name))


class LynxConfig(AppConfig):
    name = "lynx.news"
    label = "news"
    verbose_name = _("News")

    def ready(self):
        setup_app_settings()
