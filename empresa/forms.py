from django import forms
from .models import Empresa


class FormNovaEmpresa(forms.ModelForm):
    administrador = forms.CharField(label="Login administrador")
    email = forms.EmailField()
    senha = forms.CharField(label="Senha temporaria",
                            widget=forms.PasswordInput)

    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["slug_da_empresa", "criado", "ativo"]
        widgets = {
            "cnpj": forms.TextInput(attrs={"id": "cnpj"}),
            "telefone": forms.TextInput(attrs={"id": "telefone"})
        }
