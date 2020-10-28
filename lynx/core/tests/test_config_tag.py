from django.core.cache import caches
from django.db import connection, models
from django.db.models.base import ModelBase
from django.template import Context, Template
from django.test import TestCase

import pytest

from lynx.core.models import BaseConfig

pytestmark = pytest.mark.django_db


class ConfigTestCase(TestCase):

    parent = BaseConfig
    model = None

    @classmethod
    def setUpClass(cls) -> None:
        @classmethod  # noqa
        def get_initial(cls):  # noqa
            return {"id": cls.DEFAULT_PK, "flag": True}

        cls.model = ModelBase(
            "TagConfig",
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

    def test_invalid_app_name(self):
        """When loading settings, an error is raised if the app name is incorrect."""
        template = Template(
            """
            {% load configs %}
            {% config "cor.TagConfig" as settings  %}
            """
        )
        with pytest.raises(LookupError):
            template.render(Context())

    def test_invalid_model_name(self):
        """When loading settings, an error is raised if the model name is incorrect."""
        template = Template(
            """
            {% load configs %}
            {% config "core.Config" as settings  %}
            """
        )
        with pytest.raises(LookupError):
            template.render(Context())

    def test_missing_app_name(self):
        """When loading settings, an error is raised if the app name is not given."""
        template = Template(
            """
            {% load configs %}
            {% config "TagConfig" as settings  %}
            """
        )
        with pytest.raises(ValueError):
            template.render(Context())

    def test_missing_model_name(self):
        """When loading settings, an error is raised if the model name is not given."""
        template = Template(
            """
            {% load configs %}
            {% config "core" as settings  %}
            """
        )
        with pytest.raises(ValueError):
            template.render(Context())

    def test_module_name(self):
        """When loading settings, an error is raised if the module path is given."""
        template = Template(
            """
            {% load configs %}
            {% config "core.models.AppSettings" as settings  %}
            """
        )
        with pytest.raises(ValueError):
            template.render(Context())

    def test_load_settings(self):
        """The config template tag loads the correct settings."""
        template = Template(
            """
            {% load configs %}
            {% config "core.TagConfig" as settings %}
            {% if settings.flag %}True{% else %}False{% endif %}
            """
        )
        output = template.render(Context())
        assert "True" in output
