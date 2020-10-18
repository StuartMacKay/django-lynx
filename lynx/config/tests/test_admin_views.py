from django.urls import reverse

import pytest

from lynx.config.models import NewsConfig, SiteConfig

pytestmark = pytest.mark.django_db


def test_app_settings_change_view(admin_client):
    SiteConfig.create()
    url = reverse("admin:config_siteconfig_changelist")
    assert admin_client.get(url).status_code == 200


def test_news_settings_change_view(admin_client):
    NewsConfig.create()
    url = reverse("admin:config_newsconfig_changelist")
    assert admin_client.get(url).status_code == 200
