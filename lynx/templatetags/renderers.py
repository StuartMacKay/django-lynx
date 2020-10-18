import inspect
import os

from django import template
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template

register = template.Library()


class TemplateRegistry:
    template_dir = None

    def __init__(self):
        self.data = {}

    @staticmethod
    def _get_class_hierarchy(klass):
        # Get the inheritance hierarchy for form fields, leaving out object.
        classes = list(inspect.getmro(klass))
        classes.reverse()
        return classes[1:]

    def _load_template(self, klass):
        try:
            template_name = "%s.html" % klass.__name__.lower()
            template_path = os.path.join(self.template_dir, template_name)
            instance = get_template(template_path)
        except TemplateDoesNotExist:
            instance = None
        return instance

    def get_template(self, klass):

        if klass in self.data and self.data[klass]:
            return self.data[klass]

        latest = None

        for item in self._get_class_hierarchy(klass):
            if item not in self.data or not self.data[item]:
                instance = self._load_template(item)
                latest = instance or latest
                self.data[item] = latest
            else:
                latest = self.data[item]

        self.data[klass] = latest

        return latest


class FieldRendererRegistry(TemplateRegistry):
    template_dir = "forms/fields"


class WidgetRendererRegistry(TemplateRegistry):
    template_dir = "forms/widgets"


field_registry = FieldRendererRegistry()
widget_registry = WidgetRendererRegistry()


@register.simple_tag
def render_field(bound_field):
    instance = field_registry.get_template(bound_field.field.__class__)
    return instance.render({"field": bound_field})


@register.simple_tag
def render_widget(bound_field):
    instance = widget_registry.get_template(bound_field.field.widget.__class__)
    return instance.render({"field": bound_field})
