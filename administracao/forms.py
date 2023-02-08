from django import forms
from .models import Login

class FormNovoUsuario(forms.ModelForm):
    levels = (
        ('', '---------'),
        ('normal', 'normal'),
        ('adm', 'administrador'),
    )
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    level = forms.CharField(widget=forms.Select(choices=levels))

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ['user']
