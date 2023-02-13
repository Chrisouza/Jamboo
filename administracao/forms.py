from django import forms
from .models import Login

class FormNovoUsuario(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ['user']
