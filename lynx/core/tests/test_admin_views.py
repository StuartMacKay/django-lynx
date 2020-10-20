from django.urls import reverse

import pytest

from lynx.core.models import SiteConfig

pytestmark = pytest.mark.django_db


def test_app_settings_change_view(admin_client):
    SiteConfig.create()
    url = reverse("admin:core_siteconfig_changelist")
    assert admin_client.get(url).status_code == 200
