from django.utils.translation import gettext as _

import pytest

from lynx.account.forms.signup import SignupForm
from lynx.site.models import SiteConfig

pytestmark = pytest.mark.django_db


def test_signup_setting():
    """Verify SiteConfig controls whether new accounts can be created."""

    SiteConfig.create(signups=False)

    form = SignupForm(
        data={
            "username": "chunkylover57",
            "password1": "2few42tg",
            "password2": "2few42tg",
        }
    )

    assert _("account.signups.disabled") in form.errors["__all__"]
