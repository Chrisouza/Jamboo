from django import forms
from .models import Login
from empresa.models import Empresa

class FormNovoUsuario(forms.ModelForm):
    levels = (
        ('', '---------'),
        ('normal', 'normal'),
        ('adm', 'administrador'),
    )
    empresas = [(i.id, i.nome) for i in Empresa.objects.all()]
    empresa = forms.CharField(widget=forms.Select(choices=empresas))
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    level = forms.CharField(widget=forms.Select(choices=levels))

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ['user_id']
