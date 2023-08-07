from email.policy import default
from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from empresa.models import Login, Nivel, Projeto, Arquivo, Empresa, Tarefas

from index.auxiliar import *


#################################################
################# INDEX #########################
#################################################


class FormLogin(forms.Form):
    usuario = forms.CharField(label="E-mail ou Usuário", required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)


#################################################
################# ADMINITRACAO #################
#################################################
class FormNovoUsuario(forms.ModelForm):
    usuario = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    senha = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = "__all__"
        exclude = ["usuario", "empresa", "primeiro_acesso", "data_criado"]


class FormEditarUsuario(forms.ModelForm):
    nova_senha = forms.CharField(label="Nova senha")

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "nova_senha": forms.PasswordInput(attrs={"required": False})
        }


class FormNovoProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = "__all__"
        exclude = ["empresa", "slug_do_projeto", "data_criado"]


# USANDO LOCALMENTE DESCOMENTE O `widgets` E COMENTE O `file`
# USANDO ONLINE DESCOMENTE O `file` E COMENTE O `widgets`
class FormNovoArquivo(forms.ModelForm):
    file = MultipleFileField()

    class Meta:
        model = Arquivo
        fields = "__all__"
        # widgets = {"file": forms.ClearableFileInput(attrs={'multiple':True, 'allow_multiple_selected':True})}
        exclude = ["empresa", "editor", "edicao",
                   "extensao", "projeto", "data_upload"]


class FormNovoNivel(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = "__all__"
        exclude = ['data_criado']


#################################################
################# EMPRESA #######################
#################################################
class FormNovaEmpresa(forms.ModelForm):
    administrador = forms.CharField(label="Login administrador")
    email = forms.EmailField()
    senha = forms.CharField(label="Senha temporaria",
                            widget=forms.TextInput(attrs={"id": "senha"}))

    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["slug_da_empresa", "pasta", "criado", "ativo"]
        widgets = {
            "cnpj": forms.TextInput(attrs={"id": "cnpj"}),
            "telefone": forms.TextInput(attrs={"id": "telefone", "maxlength": 11})
        }

    def envia_email(self, destinatario, corpo):
        # mail = send_mail(assunto, corpo, "rcsc3w@yahoo.com.br", [destinatario])
        assunto = 'Dados de acesso ao sistema'
        # send_mail(assunto, corpo, "rcsc3w@yahoo.com.br", [destinatario])


class FormEditarEmpresaRoot(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["slug_da_empresa", "pasta", "criado", "ativo"]
        widgets = {
            "cnpj": forms.TextInput(attrs={"id": "cnpj"}),
            "telefone": forms.TextInput(attrs={"id": "telefone", "maxlength": 11})
        }


class FormEditarEmpresaAdmin(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"
        exclude = ["cnpj", "nome_da_empresa",
                   "slug_da_empresa", "pasta", "criado", "ativo"]
        widgets = {
            "cnpj": forms.TextInput(attrs={"id": "cnpj"}),
            "telefone": forms.TextInput(attrs={"id": "telefone", "maxlength": 11})
        }


class FormNovaAgenda(forms.ModelForm):

    class Meta:
        model = Tarefas
        fields = "__all__"
        exclude = ["empresa", "data"]
        widgets = {
            "inicio_data": DateInput(),
            "inicio_hora": TimeInput(),
            "fim_data": DateInput(),
            "fim_hora": TimeInput()
        }


#################################################
################# EDITOR  #######################
#################################################


class FormEditor(forms.Form):
    choices = Arquivo.objects.all()
    choices = [(f"{settings.ALLOWED_HOSTS[-1]}{file.file}",
                f"{file.file}".split("/")[-1]) for file in choices]
    # choices = [(f"{settings.ALLOWED_HOSTS[0]}{file.file}", f"{file.file}".split("/")[-1]) for file in choices]
    file_antigo = forms.CharField(
        widget=forms.Select(choices=choices))
    file_novo = forms.CharField(
        widget=forms.Select(choices=choices))
