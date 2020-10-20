from django.urls import reverse

import pytest

from ..models import SiteConfig

pytestmark = pytest.mark.django_db


def test_site_config_change_view(admin_client):
    SiteConfig.create()
    url = reverse("admin:site_siteconfig_changelist")
    assert admin_client.get(url).status_code == 200
