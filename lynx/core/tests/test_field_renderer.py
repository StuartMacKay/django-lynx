from django import forms
from django.template import Context, Template


class SampleForm(forms.Form):
    name = forms.CharField()


def test_render_field():
    template = Template(
        """
        {% load renderers %}
        {% render_field form.name %}
        """
    )
    template.render(Context(dict_={"form": SampleForm()}))
