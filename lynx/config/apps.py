from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LynxConfig(AppConfig):
    name = "lynx.config"
    label = "config"
    verbose_name = _("Configuration")
