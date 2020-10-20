from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LynxConfig(AppConfig):
    name = "lynx.site"
    label = "site"
    verbose_name = _("Site")
