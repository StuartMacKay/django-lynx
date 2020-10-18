from django.contrib import admin

from lynx.config.admin.base_config import BaseConfigAdmin
from lynx.config.models import NewsConfig


@admin.register(NewsConfig)
class NewsConfigAdmin(BaseConfigAdmin):
    pass
