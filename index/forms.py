from django import forms

class FormLogin(forms.Form):
    username = forms.CharField(label="Nome de usuario:", required=True)
    password = forms.CharField(label="Senha:", widget=forms.PasswordInput, required=True)
