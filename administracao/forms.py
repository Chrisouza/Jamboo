from django import forms
from .models import Login
from django.utils.translation import gettext_lazy as _


class FormNewUser(forms.ModelForm):
    username = forms.CharField(label=_('username'), max_length=100)
    password = forms.CharField(
        label=_('password'), max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ["user"]
