from django import forms
from empresa.models import Login, Projeto


class FormNovoUsuario(forms.ModelForm):
    usuario = forms.CharField(max_length=100)
    senha = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ["usuario", "empresa"]


class FormNovoProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = "__all__"
        exclude = ["empresa", "slug"]
