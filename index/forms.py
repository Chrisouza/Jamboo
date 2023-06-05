from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from empresa.models import Login, Nivel, Projeto, Arquivo, Empresa


#################################################
################# INDEX #########################
#################################################


class FormLogin(forms.Form):
    usuario = forms.CharField(
        label="E-mail ou Usuario", required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)


#################################################
################# ADMINSITRACAO #################
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
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["data_criado"]
        widgets = {
            "password": forms.PasswordInput
        }


class FormNovoProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = "__all__"
        exclude = ["empresa", "slug_do_projeto", "data_criado"]


class FormNovoArquivo(forms.ModelForm):
    # file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,}), required=True)

    class Meta:
        model = Arquivo
        fields = "__all__"
        widgets = {
            "file": forms.ClearableFileInput(attrs={'multiple': True})
        }
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
        send_mail(assunto, corpo, "rcsc3w@yahoo.com.br", [destinatario])


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
