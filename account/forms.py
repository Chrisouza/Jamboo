from django import forms

class FormRegistre(forms.Form):
    nome = forms.CharField(label="Nome:", min_length=6, help_text="minimo 6 caracteres", required=True)
    email = forms.EmailField(label="E-mail:", help_text="Seu melhor e-mail", required=True)
    senha = forms.CharField(label="Senha:", widget=forms.PasswordInput, min_length=8,
                            help_text="minimo 8 caracteres", required=True)
    empresa = forms.CharField(label="Nome de sua empresa")

class FormLogin(forms.Form):
    email = forms.EmailField(label="E-mail:", help_text="E-mail cadastrado", required=True)
    senha = forms.CharField(label="Senha:", widget=forms.PasswordInput, min_length=8,
                            help_text="Senha cadastrada", required=True)