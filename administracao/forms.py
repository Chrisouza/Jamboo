from django import forms
from .models import Empresa, Login

class FormNovaEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ['slug', "data_criada", 'ativo']

class FormNovoUsuario(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ['user_id']
