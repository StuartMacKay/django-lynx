# The name of the cache where the settings will be stored. Caching is
# disables if this setting is None.
SETTINGS_CACHE_NAME = "default"

# The time in seconds that the setting will be cached for.
SETTINGS_CACHE_TIMEOUT = 60 * 5

# A prefix that is added to the cache key to avoid the chance of collisions.
# This is in addition to any value defined in the KEY_PREFIX setting.
SETTINGS_CACHE_PREFIX = "settings"

# The dictionary containing the defaults for each field in a settings class.
# Each key is the class name and the value is a dict with key and values for
# each field in the model that needs a default value.
SETTINGS_DEFAULTS = {
    "SiteConfig": {
        "id": 1,
        "signups": True,
    },
    "NewsConfig": {
        "id": 1,
        "items_per_page": 30,
    },
}


__all__ = (
    "SETTINGS_CACHE_NAME",
    "SETTINGS_CACHE_TIMEOUT",
    "SETTINGS_CACHE_PREFIX",
    "SETTINGS_DEFAULTS",
)
