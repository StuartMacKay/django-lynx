from django.urls import reverse

import pytest

from lynx.site.models import SiteConfig

pytestmark = pytest.mark.django_db


def test_display(client):
    url = reverse("account_login")
    response = client.get(url)
    content = str(response.content)
    assert response.status_code == 200
    assert reverse("account_signup") in content


def test_signups_disabled(client):
    """Verify the SiteConfig controls whether the signup link is visible."""
    SiteConfig.create(signups=False)
    url = reverse("account_login")
    content = str(client.get(url).content)
    assert reverse("account_signup") not in content
