from pytest_factoryboy import register

from lynx.factories import UserFactory
from lynx.news.factories import NewsFactory

pytest_plugins = [
    "lynx.fixtures",
]

register(NewsFactory)
register(UserFactory)
