import pytest

from lynx.news.forms import NewsForm

pytestmark = pytest.mark.django_db


def test_title_field_is_required(faker):
    form = NewsForm(data={"title": "", "url": faker.url()})
    assert not form.is_valid()
    assert "title" in form.errors


def test_url_field_is_required(faker):
    form = NewsForm(data={"title": faker.text(), "url": ""})
    assert not form.is_valid()
    assert "url" in form.errors
