from django.contrib import admin

from lynx.core.admin.base_config import BaseConfigAdmin

from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(BaseConfigAdmin):
    pass
