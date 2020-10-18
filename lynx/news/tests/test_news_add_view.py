from django.conf import settings
from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_display(user_client):
    user, client = user_client()
    url = reverse("news:add-item")
    assert client.get(url).status_code == 200


def test_login_required(client):
    url = reverse("news:add-item")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(settings.LOGIN_URL)
