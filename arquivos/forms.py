from django import forms
from .models import Arquivo

class FormAdicionaArquivo(forms.Form):
    arquivo = forms.FileField()