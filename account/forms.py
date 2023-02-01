from django import forms

from .models import Foto
from django.contrib.auth.models import User

class FormRegistre(forms.Form):
    nome = forms.CharField(label="Nome:", required=True)
    username = forms.CharField(label="Nome de usuario:", min_length=6, help_text="minimo 6 caracteres", required=True)
    email = forms.EmailField(label="E-mail:", help_text="Seu melhor e-mail", required=True)
    senha = forms.CharField(label="Senha:", widget=forms.PasswordInput, min_length=8,
                            help_text="minimo 8 caracteres", required=True)


class FormLogin(forms.Form):
    username = forms.CharField(label="Nome de usuario:", min_length=6, required=True)
    senha = forms.CharField(label="Senha:", widget=forms.PasswordInput, min_length=8,
                            help_text="Senha cadastrada", required=True)


class FormFoto(forms.ModelForm):
    class Meta:
        model = Foto
        fields = "__all__"
        exclude = ["id_usuario"]
        widgets = {
            'foto':forms.FileInput
        }

class FormSenhaUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password"]
        widgets = {
            'password':forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super(FormSenhaUpdate, self).__init__(*args, **kwargs)

        for fieldname in ['password']:
            self.fields[fieldname].help_text = None

