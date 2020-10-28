from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.account import forms

from lynx.site.models import SiteConfig

from .utils import remove_placeholders


class SignupForm(forms.SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        remove_placeholders(self)

    def clean(self):
        super(SignupForm, self).clean()

        if not SiteConfig.fetch().signups:
            raise ValidationError(_("account.signups.disabled"))
