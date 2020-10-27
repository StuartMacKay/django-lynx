from django.urls import reverse

import pytest

from lynx.news.models import NewsConfig

pytestmark = pytest.mark.django_db


def test_display(client, news_factory):
    news_factory.create()
    url = reverse("news:list-items")
    response = client.get(url)
    assert response.status_code == 200


def test_pagination(client, news_factory):
    page_size = NewsConfig.fetch().items_per_page
    news_factory.create_batch(page_size * 2)

    url = reverse("news:list-items")
    response = client.get(url)
    content = str(response.content)
    page = response.context["page_obj"]
    paginator = page.paginator

    assert page.number == 1
    assert paginator.count == page_size * 2
    assert paginator.per_page == page_size
    assert paginator.num_pages == 2
    assert "?page=%d" % (page.number + 1) in content

