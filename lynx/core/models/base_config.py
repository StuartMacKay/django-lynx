"""
Model for cresting singletons for storing configurations in the database.

Todo:
    * There are still a couple of inconsistencies between the way objects
      behave with the cache and the database. For example, you can delete
      an object from the database but still add it to the cache.
    * Should the cache key use the object's actual pk rather than the
      assumed value (the default from the config values or the DEFAULT_PK value.

"""
from typing import Tuple, Type

from django.conf import settings
from django.core.cache import caches
from django.db import models

__all__ = ("BaseConfig",)


class BaseConfig(models.Model):

    # The name of the cache where the object will be stored. Caching is
    # disables if this setting is None.
    CONFIG_CACHE_NAME = "default"

    # The time in seconds that the setting will be cached for.
    CONFIG_CACHE_TIMEOUT = 60 * 5

    # A prefix that is added to the cache key to avoid the chance of collisions.
    # This is in addition to any value defined in the KEY_PREFIX setting.
    CONFIG_CACHE_PREFIX = "config"

    CACHE_NAME = "CONFIG_CACHE_NAME"
    CACHE_TIMEOUT = "CONFIG_CACHE_TIMEOUT"
    CACHE_PREFIX = "CONFIG_CACHE_PREFIX"
    DEFAULTS = "CONFIG_DEFAULTS"

    DEFAULT_PK = 1

    class Meta:
        abstract = True

    @classmethod
    def get_setting(cls, name):
        return getattr(settings, name, getattr(cls, name))

    @classmethod
    def get_initial(cls) -> dict:
        return {
            "id": cls.DEFAULT_PK,
        }

    @classmethod
    def get_site_defaults(cls):
        defaults = getattr(settings, cls.DEFAULTS, {})
        return defaults.get(cls.__name__, {})

    @classmethod
    def get_defaults(cls, **kwargs) -> dict:
        """
        Get the default values for each field in the model.

        """
        defaults = cls.get_initial()
        defaults.update(cls.get_site_defaults())
        defaults.update(kwargs)
        return defaults

    @classmethod
    def get_pk(cls) -> int:
        return cls.get_defaults().get("id", cls.DEFAULT_PK)

    @classmethod
    def get_cache_name(cls) -> str:
        return cls.get_setting(cls.CACHE_NAME)

    @classmethod
    def get_cache_timeout(cls) -> int:
        return cls.get_setting(cls.CACHE_TIMEOUT)

    @classmethod
    def get_cache_prefix(cls) -> str:
        return cls.get_setting(cls.CACHE_PREFIX)

    @classmethod
    def get_cache_key(cls) -> str:
        return "%s:%s:%d" % (cls.get_cache_prefix(), cls.__name__.lower(), cls.get_pk())

    @classmethod
    def get_cache(cls):
        name = cls.get_cache_name()
        return caches[name] if name else None

    @classmethod
    def get_cache_entry(cls) -> (Type["BaseConfig"], None):
        """Get the config object from the cache."""
        cache = cls.get_cache()
        return cache.get(cls.get_cache_key()) if cache else None

    @classmethod
    def create(cls, **kwargs):
        """
        Create/re-generate the config object from the defaults.

        """
        obj = cls(**cls.get_defaults(**kwargs))
        obj.save()
        return obj

    @classmethod
    def fetch(cls):
        """
        Fetch the config singleton returning it from the cache, if enabled,
        otherwise the database.

        """
        obj = cls.get_cache_entry()
        if obj is None:  # cache miss
            obj = cls.objects.first()
            if obj is None:  # database miss
                obj = cls.create()
            else:
                obj.cache()
        return obj

    def __str__(self) -> str:
        return "%s" % self._meta.verbose_name

    def save(self, *args, **kwargs) -> None:
        """
        Save the config to the database and update the cache, if enabled.

        Notes:
            The primary key is set explicitly to prevent multiple instances
            from being created. This could happen with modelform_factory in
            the Django Admin since it ignores any primary key value defined
            in the defaults.

            Since this is an abstract class it's much easier to simply override
            save() rather than use the pre_save signal.

        """
        self.pk = self.get_pk()
        super(BaseConfig, self).save(*args, **kwargs)
        self.cache()

    def delete(self, *args, **kwargs) -> Tuple[int, dict]:
        """Delete the object from the database and the cache, if enabled."""
        self.purge()
        return super(BaseConfig, self).delete(*args, **kwargs)

    def cache(self) -> None:
        """Add the object to the cache, if enabled."""
        cache = self.get_cache()
        if cache:
            key = self.get_cache_key()
            timeout = self.get_cache_timeout()
            cache.set(key, self, timeout)

    def purge(self) -> None:
        """Delete the object from the cache, if enabled."""
        cache = self.get_cache()
        if cache:
            # Fails silently if the object does not exist.
            cache.delete(self.get_cache_key())
