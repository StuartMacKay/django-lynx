from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def config(model_path):
    """
    Load the config object for a given app.

    Args:
        model_path: the path to the settings Model in the form
        <app_name>.<model name>, e.g. site.SiteConfig.

    Returns:
        The settings object for the app.

    Examples:
        The settings object is loaded using the Django model dotted path:::

            {% load configs %}
            {% config site.SiteConfig as settings %}
            {{ settings.signups }}

    Raises:
        LookupError: if the path does not match an existing Django app or
            model name.
        ValueError: if the path does not follow Django model dotted path,
            <app_name>.<model name>.

    """
    return apps.get_model(model_path).fetch()
