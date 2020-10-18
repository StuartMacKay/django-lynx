from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_config import BaseConfig


class SiteConfig(BaseConfig):

    signups = models.BooleanField(default=True)

    signups.verbose_name = _("Enable signups")

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")
