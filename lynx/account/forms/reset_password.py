from allauth.account import forms

from .utils import remove_placeholders


class ResetPasswordForm(forms.ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        remove_placeholders(self)
