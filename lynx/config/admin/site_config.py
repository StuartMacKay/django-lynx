from django.contrib import admin

from lynx.config.admin.base_config import BaseConfigAdmin
from lynx.config.models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(BaseConfigAdmin):
    pass
