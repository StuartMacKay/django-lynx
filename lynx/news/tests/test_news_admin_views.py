from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_news_item_changelist_view(admin_client, news_factory):
    news_factory.create()
    url = reverse("admin:news_news_changelist")
    assert admin_client.get(url).status_code == 200


def test_news_item_add_view(admin_client):
    url = reverse("admin:news_news_add")
    assert admin_client.get(url).status_code == 200
