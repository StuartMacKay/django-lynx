from django.core.cache import InvalidCacheBackendError, caches

import pytest

from lynx.config import settings as app_settings
from lynx.config.models import SiteConfig

pytestmark = pytest.mark.django_db


def get_database_entry() -> SiteConfig:
    """Get the settings object from the database."""
    return SiteConfig.objects.first()


def set_database_entry(**kwargs) -> None:
    """Add the settings object to the database but not the cache."""
    obj = SiteConfig.objects.create(**SiteConfig.get_defaults(**kwargs))
    obj.purge()


def get_cache_entry() -> SiteConfig:
    """Get the settings from the cache, if it exists."""
    cache_key = SiteConfig.get_cache_key()
    return caches[SiteConfig.get_cache_name()].get(cache_key)


def set_cache_entry(**kwargs) -> None:
    """Add the settings object to the cache but not the database."""
    name = SiteConfig.get_cache_name()
    key = SiteConfig.get_cache_key()
    timeout = SiteConfig.get_cache_timeout()
    obj = SiteConfig(**kwargs)
    caches[name].set(key, obj, timeout)


def setup_function(function):  # noqa
    """Setup for each test.

    Notes:
        All settings objects are deleted from the database and the cache
        is cleared before the start of each test. Pytest-django clears
        the database the same way Django's TestCase does but we do the
        delete here to make the starting state for the tests clear.

    """
    SiteConfig.objects.all().delete()
    caches[SiteConfig.get_cache_name()].clear()


#
# Tests for the get_settings() class method.
#


def test_get_app_setting_local():
    """Verify get_setting() fetches the setting from the local settings.py."""
    setting = SiteConfig.get_setting(SiteConfig.CACHE_NAME)
    assert setting == app_settings.SETTINGS_CACHE_NAME


def test_site_setting_overrides_app_setting(settings):
    """Verify get_setting() returns the setting from Django settings if defined."""
    settings.SETTINGS_CACHE_NAME = "other"
    setting = SiteConfig.get_setting(SiteConfig.CACHE_NAME)
    assert setting == "other" != app_settings.SETTINGS_CACHE_NAME


def test_missing_setting_raises_error():
    """Ensure get_setting() raises an error is the setting is undefined."""
    with pytest.raises(AttributeError):
        SiteConfig.get_setting("missing")


#
# Tests for the get_defaults() class method.
#


def test_app_settings_defaults():
    """Verify get_defaults() returns the default field value from the local settings.py"""
    assert SiteConfig.get_defaults() == app_settings.SETTINGS_DEFAULTS["SiteConfig"]


def test_get_defaults_returns_app():
    """Verify that get_defaults() returns values for all the model fields."""
    defaults = SiteConfig.get_defaults()
    for field in SiteConfig._meta.fields:
        assert field.name in defaults


def test_get_defaults_creates_copy():
    """Verify get_defaults() returns a copy of the default settings."""
    SiteConfig.get_defaults()["added"] = "value"
    assert "added" not in SiteConfig.get_defaults()


def test_defaults_overridden_by_site_settings(settings):
    """Verify the Django settings override the values from the app's settings.py."""
    settings.SETTINGS_DEFAULTS = {"SiteConfig": {"signups": False}}
    defaults = SiteConfig.get_defaults()
    assert not defaults["signups"]


def test_defaults_kwargs_overrides_site_settings(settings):
    """Verify values passed as kwargs to get_defaults() have highest priority."""
    settings.SIGNUPS = True
    defaults = SiteConfig.get_defaults(signups=False)
    assert not defaults["signups"]


#
# Tests for get_pk() class method.
#


def test_get_pk_default():
    """Verify get_pk() returns the values from the defaults."""
    assert app_settings.SETTINGS_DEFAULTS["SiteConfig"]["id"] == SiteConfig.get_pk()


def test_get_pk_missing():
    """Verify get_pk() return the default value on the class if not in the defaults"""
    value = app_settings.SETTINGS_DEFAULTS["SiteConfig"]["id"]
    del app_settings.SETTINGS_DEFAULTS["SiteConfig"]["id"]
    assert SiteConfig.get_pk() == SiteConfig.DEFAULT_PK
    app_settings.SETTINGS_DEFAULTS["SiteConfig"]["id"] = value


#
# Tests for the get_cache() and get_cache_entry() class methods.
#


def test_get_cache_returns_cache():
    """Verify get_cache() returns the cache for settings."""
    assert "default" == SiteConfig.get_cache_name()
    assert caches["default"] == SiteConfig.get_cache()


def test_none_returned_if_caching_disabled(settings):
    """Verify setting SETTINGS_CACHE_NAME to None disables caching."""
    settings.SETTINGS_CACHE_NAME = None
    assert SiteConfig.get_cache() is None


def test_none_returned_if_caching_undefined(settings):
    """Verify an error is raised if the wrong cache name is used."""
    with pytest.raises(InvalidCacheBackendError):
        settings.SETTINGS_CACHE_NAME = "other"
        assert SiteConfig.get_cache() is None


def test_get_entry_from_cache():
    """Verify get_cache_entry() returns settings object from cache."""
    set_cache_entry(**SiteConfig.get_defaults())
    assert SiteConfig.get_cache_entry() is not None


def test_get_entry_from_cache_with_cache_disabled(settings):
    """Verify get_cache_entry() returns None if cache is disabled."""
    set_cache_entry(**SiteConfig.get_defaults())
    settings.SETTINGS_CACHE_NAME = None
    assert SiteConfig.get_cache_entry() is None


#
# Tests for the create() class method.
#


def test_create_saves_instance():
    """Verify create() adds the object to the database."""
    SiteConfig.create()
    assert get_database_entry() is not None


def test_create_caches_instance():
    """Verify create() adds the object to the cache."""
    SiteConfig.create()
    assert get_cache_entry() is not None


def test_create_overwrites_instance():
    """Calling create() multiple times overwrites existing instance."""
    SiteConfig.create()
    SiteConfig.create(signups=False)
    assert SiteConfig.objects.count() == 1
    assert not get_database_entry().signups


def test_create_with_cache_disabled(settings):
    """Verify create() skips updating the cache."""
    cache_name = SiteConfig.get_cache_name()
    settings.SETTINGS_CACHE_NAME = None
    SiteConfig.create()
    settings.SETTINGS_CACHE_NAME = cache_name
    assert get_cache_entry() is None


#
# Tests for the fetch() class method.
#


def test_fetch_with_cache_hit(django_assert_num_queries):
    """The settings object is fetched from the cache, if enabled."""
    set_database_entry(signups=True)
    set_cache_entry(signups=False)
    with django_assert_num_queries(0):
        config = SiteConfig.fetch()
    assert not config.signups


def test_fetch_with_cache_miss(django_assert_num_queries):
    """The settings object is fetched from the database on cache miss."""
    set_database_entry(signups=False)
    with django_assert_num_queries(1):
        obj = SiteConfig.fetch()
    assert not obj.signups


def test_fetch_with_cache_disabled(settings, django_assert_num_queries):
    """The settings object is fetched from the database if the cache is disabled."""
    set_database_entry(signups=False)
    set_cache_entry(signups=True)
    settings.SETTINGS_CACHE_NAME = None
    with django_assert_num_queries(1):
        obj = SiteConfig.fetch()
    assert not obj.signups


def test_fetch_creates_object(django_assert_num_queries):
    """On a cache and database miss fetch() creates the settings object."""
    with django_assert_num_queries(3):
        obj = SiteConfig.fetch()
    assert obj.signups == SiteConfig.get_defaults()["signups"]
    assert get_cache_entry() is not None


#
# Tests for the model related save() and delete() methods.
#


def test_save_sets_primary_key():
    """Even if the primary key is overridden it is set when the settings are saved."""
    obj = SiteConfig.create(id=2)
    assert obj.id == obj.get_pk() != 2


def test_save_adds_to_cache():
    """The save() adds the object to the cache."""
    SiteConfig.create()
    assert get_cache_entry() is not None


def test_save_updates_cache():
    """The save() overwrites any existing entry in the cache."""
    set_cache_entry(signups=True)
    SiteConfig.create(signups=False)
    assert not get_cache_entry().signups


def test_delete_from_database():
    """The delete() method deletes the object from the database."""
    obj = SiteConfig.create()
    obj.delete()
    assert SiteConfig.objects.count() == 0


def test_delete_from_cache():
    """The delete() method purges the object from the cache."""
    obj = SiteConfig.fetch()
    obj.delete()
    assert get_cache_entry() is None


#
# Tests for the cache related cache() and purge() methods.
#


def test_cache_updates_cache():
    """Verify cache() adds an object to the cache."""
    obj = SiteConfig(**SiteConfig.get_defaults())
    obj.cache()
    assert get_cache_entry() is not None


def test_cache_with_cache_disabled(settings):
    """Verify cache() has no effect if cache is disabled."""
    obj = SiteConfig(**SiteConfig.get_defaults())
    cache_name = SiteConfig.get_cache_name()
    settings.SETTINGS_CACHE_NAME = None
    obj.cache()
    settings.SETTINGS_CACHE_NAME = cache_name
    assert get_cache_entry() is None


def test_purge_clears_cache():
    """Verify purge() deletes the entry from the cache."""
    SiteConfig.create().purge()
    assert get_cache_entry() is None


def test_purge_with_cache_disabled(settings):
    """Verify purge() has no effect if cache is disabled."""
    obj = SiteConfig.create()
    cache_name = SiteConfig.get_cache_name()
    settings.SETTINGS_CACHE_NAME = None
    obj.purge()
    settings.SETTINGS_CACHE_NAME = cache_name
    assert get_cache_entry() is not None
