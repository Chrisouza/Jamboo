from django import forms
from .models import Empresa
from django.core.mail import EmailMessage


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

    def send_email(assunto, destinatario, corpo):
        mail = EmailMessage(
            object=assunto,
            from_email="rcsc3w@yahoo.com.br",
            to=[destinatario,],
            body=corpo,
            headers={
                "Replay": "rcsc3w@yahoo.com.br"
            }
        )
        mail.send()
