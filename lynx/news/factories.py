from datetime import datetime, timedelta
from random import randrange

import factory

from lynx.core.factories import UserFactory


def relative_date(delta):
    seconds = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(abs(seconds))
    if seconds < 0:
        random_second = -random_second
    return datetime.utcnow() + timedelta(seconds=random_second)


def recent():
    return relative_date(-timedelta(days=7))


class NewsFactory(factory.django.DjangoModelFactory):

    timestamp = factory.LazyFunction(recent)

    created = factory.LazyAttribute(lambda o: o.timestamp)
    updated = factory.LazyAttribute(lambda o: o.timestamp)

    title = factory.Faker("sentence")
    url = factory.Faker("url")

    submitted_by = factory.SubFactory(UserFactory)

    class Meta:
        model = "news.News"
        exclude = ("timestamp",)
