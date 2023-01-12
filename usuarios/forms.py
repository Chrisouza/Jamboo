from django import forms

class UserForm(forms.Form):
    #foto = forms.ImageField()
    username = forms.CharField(label="Nome de usuario:", required=True)
    email = forms.EmailField(label="E-mail:", required=True)
    password = forms.CharField(label="Senha:", widget=forms.PasswordInput, required=True)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)