from django import forms
from .models import Administrador

class FormNovoAdm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = "__all__"
        exclude = ['ativo', 'adm', 'logado']
        widgets = {
            'senha':forms.PasswordInput
        }
