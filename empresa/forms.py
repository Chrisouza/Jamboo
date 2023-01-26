from django import forms
from empresa.models import Empresa

class FormNovaEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ['id_adm']