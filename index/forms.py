from django import forms
from django.utils.translation import gettext_lazy as _


class FormLogin(forms.Form):
    username = forms.CharField(label=_("username"), required=True)
    password = forms.CharField(
        label=_("password"), widget=forms.PasswordInput, required=True)
