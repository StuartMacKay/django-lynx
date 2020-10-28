from allauth.account import forms

from .utils import remove_placeholders


class SigninForm(forms.LoginForm):

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        remove_placeholders(self)
