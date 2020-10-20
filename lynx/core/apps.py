from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LynxConfig(AppConfig):
    name = "lynx.core"
    label = "core"
    verbose_name = _("Core")
