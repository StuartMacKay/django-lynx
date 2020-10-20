from pytest_factoryboy import register

from lynx.core.factories import UserFactory
from lynx.news.factories import NewsFactory

pytest_plugins = [
    "lynx.core.fixtures",
]

register(NewsFactory)
register(UserFactory)
