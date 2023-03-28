from django import forms
from .models import Empresa


class FormNovaEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["slug", "criado", "ativo"]
