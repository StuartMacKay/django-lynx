from django.db import models
from django.utils.translation import gettext_lazy as _

from lynx.core.models import BaseConfig


class SiteConfig(BaseConfig):

    TITLE = "Django Lynx"
    SIGNUPS = True

    title = models.CharField(max_length=50, blank=True)
    logo = models.FileField(upload_to="site", null=True)
    icon = models.FileField(upload_to="site", null=True)
    signups = models.BooleanField(default=True)

    title.verbose_name = _("Site title")
    logo.verbose_name = _("Site logo")
    icon.verbose_name = _("Site favicon")
    signups.verbose_name = _("Enable signups")

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")

    @classmethod
    def get_initial(cls):
        initial = super().get_initial()
        initial["title"] = cls.TITLE
        initial["signups"] = cls.SIGNUPS
        return initial
