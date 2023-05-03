from django import forms
from .models import Empresa
from django.core.mail import send_mail


class FormNovaEmpresa(forms.ModelForm):
    administrador = forms.CharField(label="Login administrador")
    email = forms.EmailField()
    senha = forms.CharField(label="Senha temporaria",
                            widget=forms.TextInput(attrs={"id": "senha"}))

    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["slug_da_empresa", "criado", "ativo"]
        widgets = {
            "cnpj": forms.TextInput(attrs={"id": "cnpj"}),
            "telefone": forms.TextInput(attrs={"id": "telefone"})
        }

    def envia_email(self, destinatario, corpo):
        # mail = send_mail(assunto, corpo, "rcsc3w@yahoo.com.br", [destinatario])
        assunto = 'Dados de acesso ao sistema'
        send_mail(assunto, corpo, "rcsc3w@yahoo.com.br", [destinatario])
