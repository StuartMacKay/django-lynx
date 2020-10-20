from django.contrib import admin

from lynx.config.admin.base_config import BaseConfigAdmin

from .models import News, NewsConfig


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = ("title", "submitted_by")


@admin.register(NewsConfig)
class NewsConfigAdmin(BaseConfigAdmin):
    pass
