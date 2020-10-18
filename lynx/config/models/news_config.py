from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_config import BaseConfig


class NewsConfig(BaseConfig):

    items_per_page = models.IntegerField()

    items_per_page.verbose_name = _("News items per page")

    class Meta:
        verbose_name = _("News Configuration")
        verbose_name_plural = _("News Configuration")
