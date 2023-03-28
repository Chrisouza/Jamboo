from django import forms


class FormLogin(forms.Form):
    usuario = forms.CharField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)
