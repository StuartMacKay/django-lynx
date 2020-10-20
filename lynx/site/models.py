from django.db import models
from django.utils.translation import gettext_lazy as _

from lynx.core.models import BaseConfig


class SiteConfig(BaseConfig):

    SIGNUPS = True

    signups = models.BooleanField(default=True)

    signups.verbose_name = _("Enable signups")

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")

    @classmethod
    def get_initial(cls):
        initial = super().get_initial()
        initial["signups"] = cls.SIGNUPS
        return initial
