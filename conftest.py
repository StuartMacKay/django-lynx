from pytest_factoryboy import register

from lynx.factories import UserFactory

pytest_plugins = [
    "lynx.tests.fixtures",
]

register(UserFactory)
