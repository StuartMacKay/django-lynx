from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_display(client, news_factory):
    news_factory.create()
    url = reverse("news:list-items")
    response = client.get(url)
    assert response.status_code == 200
