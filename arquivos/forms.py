from django import forms
from .models import Arquivo

class FormArquivo(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ["file"]