from django.conf import settings
from django.core.cache import InvalidCacheBackendError, caches
from django.db import connection, models
from django.db.models.base import ModelBase
from django.test import TestCase

import pytest

from lynx.config.models import BaseConfig

# These tests were originally written as pytest functions however there
# were problems creating the concrete class for testing - specifically
# sqlite3 did not allow the schema editor to run while the transaction
# pytest-django created was active. There was not enough time to look into
# this in more detail so we just went with the Django TestCase.
#
# The site settings are accessed using getattr() so that rules out using
# the TestCase method settings() to temporarily change them.


class ConfigTestCase(TestCase):

    parent = BaseConfig
    model = None

    @classmethod
    def setUpClass(cls) -> None:
        @classmethod  # noqa
        def get_initial(cls):  # noqa
            return {"id": cls.DEFAULT_PK, "flag": True}

        cls.model = ModelBase(
            "TestConfig",
            (cls.parent,),
            {
                "__module__": cls.parent.__module__,
                "flag": models.BooleanField(default=True),
            },
        )

        setattr(cls.model, "get_initial", get_initial)

        with connection.schema_editor() as editor:
            editor.create_model(cls.model)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        with connection.schema_editor() as editor:
            editor.delete_model(cls.model)
        connection.close()

    def setUp(self):
        cache_name = self.model.get_cache_name()
        if cache_name:
            caches[cache_name].clear()

    def get_database_entry(self):
        """Get the settings object from the database."""
        return self.model.objects.first()

    def set_database_entry(self, **kwargs):
        """Add the settings object to the database but not the cache."""
        obj = self.model.objects.create(**self.model.get_defaults(**kwargs))
        obj.purge()

    def get_cache_entry(self):
        """Get the settings from the cache, if it exists."""
        cache_key = self.model.get_cache_key()
        return caches[self.model.get_cache_name()].get(cache_key)

    def set_cache_entry(self, **kwargs):
        """Add the settings object to the cache but not the database."""
        name = self.model.get_cache_name()
        key = self.model.get_cache_key()
        timeout = self.model.get_cache_timeout()
        obj = self.model(**kwargs)
        caches[name].set(key, obj, timeout)

    #
    # Tests for the get_settings() class method.
    #

    def test_site_setting_overrides_attribute(self):
        """Verify get_setting() returns the setting from Django settings if defined."""
        settings.CONFIG_CACHE_NAME = "other"
        setting = self.model.get_setting(self.model.CACHE_NAME)
        del settings.CONFIG_CACHE_NAME
        self.assertEqual(setting, "other")
        self.assertNotEqual(setting, self.model.CONFIG_CACHE_NAME)

    def test_missing_setting_raises_error(self):
        """Ensure get_setting() raises an error is the setting is undefined."""
        with pytest.raises(AttributeError):
            self.model.get_setting("missing")

    #
    # Tests for the get_defaults() class method.
    #

    def test_get_defaults(self):
        """Verify get_defaults() returns the initial field values"""
        self.assertEqual(self.model.get_defaults(), self.model.get_initial())

    def test_get_defaults_fields(self):
        """Verify that get_defaults() returns values for all the model fields."""
        defaults = self.model.get_defaults()
        for field in self.model._meta.fields:
            self.assertTrue(field.name in defaults)

    def test_get_defaults_creates_copy(self):
        """Verify get_defaults() returns a copy of the default settings."""
        self.model.get_defaults()["added"] = "value"
        self.assertFalse("added" in self.model.get_defaults())

    def test_defaults_overridden_by_site_settings(self):
        """Verify the Django settings override the values from Django's settings."""
        settings.CONFIG_DEFAULTS = {"TestConfig": {"flag": False}}
        defaults = self.model.get_defaults()
        del settings.CONFIG_DEFAULTS
        self.assertFalse(defaults["flag"])

    def test_defaults_kwargs_overrides_site_settings(self):
        """Verify values passed as kwargs to get_defaults() have highest priority."""
        settings.CONFIG_DEFAULTS = {"TestConfig": {"flag": True}}
        defaults = self.model.get_defaults(flag=False)
        del settings.CONFIG_DEFAULTS
        self.assertFalse(defaults["flag"])

    #
    # Tests for get_pk() class method.
    #

    def test_get_pk_attribute(self):
        """Verify get_pk() returns attribute."""
        self.model.DEFAULT_PK = 42
        self.assertEqual(self.model.get_pk(), 42)

    def test_get_pk_in_defaults(self):
        """Verify get_pk() returns the values from the defaults."""
        self.assertEqual(self.model.get_defaults()["id"], self.model.get_pk())

    def test_get_pk_defaults_overridden_by_site_settings(self):
        """Verify get_pk() """
        settings.CONFIG_DEFAULTS = {"TestConfig": {"id": 42}}
        self.assertEqual(self.model.get_pk(), 42)
        del settings.CONFIG_DEFAULTS

    #
    # Tests for the get_cache() and get_cache_entry() class methods.
    #

    def test_get_cache_returns_cache(self):
        """Verify get_cache() returns the cache for settings."""
        self.assertEqual("default", self.model.get_cache_name())
        self.assertEqual(caches["default"], self.model.get_cache())

    def test_none_returned_if_caching_disabled(self):
        """Verify setting CONFIG_CACHE_NAME to None disables caching."""
        settings.CONFIG_CACHE_NAME = None
        self.assertIsNone(self.model.get_cache())
        del settings.CONFIG_CACHE_NAME

    def test_none_returned_if_caching_undefined(self):
        """Verify an error is raised if the wrong cache name is used."""
        settings.CONFIG_CACHE_NAME = "other"
        with pytest.raises(InvalidCacheBackendError):
            self.assertIsNone(self.model.get_cache())
        del settings.CONFIG_CACHE_NAME

    def test_get_entry_from_cache(self):
        """Verify get_cache_entry() returns settings object from cache."""
        self.set_cache_entry(**self.model.get_defaults())
        self.assertIsNotNone(self.model.get_cache_entry())

    def test_get_entry_from_cache_with_cache_disabled(self):
        """Verify get_cache_entry() returns None if cache is disabled."""
        self.set_cache_entry(**self.model.get_defaults())
        settings.CONFIG_CACHE_NAME = None
        self.assertIsNone(self.model.get_cache_entry())
        del settings.CONFIG_CACHE_NAME

    #
    # Tests for the create() class method.
    #

    def test_create_saves_instance(self):
        """Verify create() adds the object to the database."""
        self.model.create()
        self.assertIsNotNone(self.get_database_entry())

    def test_create_caches_instance(self):
        """Verify create() adds the object to the cache."""
        self.model.create()
        self.assertIsNotNone(self.get_cache_entry())

    def test_create_overwrites_instance(self):
        """Calling create() multiple times overwrites existing instance."""
        self.model.create()
        self.model.create(flag=False)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertFalse(self.get_database_entry().flag)

    def test_create_with_cache_disabled(self):
        """Verify create() skips updating the cache."""
        settings.CONFIG_CACHE_NAME = None
        self.model.create()
        del settings.CONFIG_CACHE_NAME
        self.assertIsNone(self.get_cache_entry())

    #
    # Tests for the fetch() class method.
    #

    def test_fetch_with_cache_hit(self):
        """The settings object is fetched from the cache, if enabled."""
        self.set_database_entry(flag=True)
        self.set_cache_entry(flag=False)
        with self.assertNumQueries(0):
            obj = self.model.fetch()
        self.assertFalse(obj.flag)

    def test_fetch_with_cache_miss(self):
        """The settings object is fetched from the database on cache miss."""
        self.set_database_entry(flag=False)
        with self.assertNumQueries(1):
            obj = self.model.fetch()
        self.assertFalse(obj.flag)

    def test_fetch_with_cache_disabled(self):
        """The settings object is fetched from the database if the cache is disabled."""
        self.set_database_entry(flag=False)
        self.set_cache_entry(flag=True)
        settings.CONFIG_CACHE_NAME = None
        with self.assertNumQueries(1):
            obj = self.model.fetch()
        del settings.CONFIG_CACHE_NAME
        self.assertFalse(obj.flag)

    def test_fetch_creates_object(self):
        """On a cache and database miss fetch() creates the settings object."""
        with self.assertNumQueries(3):
            obj = self.model.fetch()
        self.assertEqual(obj.flag, self.model.get_defaults()["flag"])
        self.assertIsNotNone(self.get_cache_entry())

    #
    # Tests for the model related save() and delete() methods.
    #

    def test_save_sets_primary_key(self):
        """Even if the primary key is overridden it is set when the settings are saved."""
        obj = self.model.create(id=2)
        assert obj.id == obj.get_pk() != 2

    def test_save_adds_to_cache(self):
        """The save() adds the object to the cache."""
        self.model.create()
        self.assertIsNotNone(self.get_cache_entry())

    def test_save_updates_cache(self):
        """The save() overwrites any existing entry in the cache."""
        self.set_cache_entry(flag=True)
        self.model.create(flag=False)
        self.assertFalse(self.get_cache_entry().flag)

    def test_delete_from_database(self):
        """The delete() method deletes the object from the database."""
        obj = self.model.create()
        obj.delete()
        self.assertEqual(self.model.objects.count(), 0)

    def test_delete_from_cache(self):
        """The delete() method purges the object from the cache."""
        obj = self.model.fetch()
        obj.delete()
        self.assertIsNone(self.get_cache_entry())

    #
    # Tests for the cache related cache() and purge() methods.
    #

    def test_cache_updates_cache(self):
        """Verify cache() adds an object to the cache."""
        obj = self.model(**self.model.get_defaults())
        obj.cache()
        self.assertIsNotNone(self.get_cache_entry())

    def test_cache_with_cache_disabled(self):
        """Verify cache() has no effect if cache is disabled."""
        obj = self.model(**self.model.get_defaults())
        settings.CONFIG_CACHE_NAME = None
        obj.cache()
        del settings.CONFIG_CACHE_NAME
        self.assertIsNone(self.get_cache_entry())

    def test_purge_clears_cache(self):
        """Verify purge() deletes the entry from the cache."""
        self.model.create().purge()
        self.assertIsNone(self.get_cache_entry())

    def test_purge_with_cache_disabled(self):
        """Verify purge() has no effect if cache is disabled."""
        obj = self.model.create()
        settings.CONFIG_CACHE_NAME = None
        obj.purge()
        del settings.CONFIG_CACHE_NAME
        self.assertIsNotNone(self.get_cache_entry())
