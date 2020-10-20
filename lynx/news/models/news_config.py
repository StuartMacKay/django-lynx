from django.db import models
from django.utils.translation import gettext_lazy as _

from lynx.config.models.base_config import BaseConfig


class NewsConfig(BaseConfig):

    ITEMS_PER_PAGE = 30

    items_per_page = models.IntegerField()

    items_per_page.verbose_name = _("News items per page")

    class Meta:
        verbose_name = _("News Configuration")
        verbose_name_plural = _("News Configuration")

    @classmethod
    def get_initial(cls):
        initial = super().get_initial()
        initial["items_per_page"] = cls.ITEMS_PER_PAGE
        return initial
