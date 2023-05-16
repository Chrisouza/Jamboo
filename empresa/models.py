from django.db import models
from django.forms import Widget
from django.utils import timezone
from django.contrib.auth.models import User


class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, default="", unique=True)
    slug_da_empresa = models.CharField(max_length=255, default="", unique=True)
    nome_da_empresa = models.CharField(max_length=255, default="", unique=True)
    nome_do_responsavel = models.CharField(
        max_length=255, default="", unique=True)
    telefone = models.CharField(max_length=16, default="", unique=True)
    criado = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome_da_empresa


class Nivel(models.Model):
    nome_do_nivel = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "nivel"
        verbose_name = "Nivel"
        verbose_name_plural = "Niveis"

    def __str__(self) -> str:
        return self.nome_do_nivel


class Login(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)
    primeiro_acesso = models.BooleanField(default=False)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    def __str__(self):
        return f"{self.usuario.username}"


class Projeto(models.Model):
    slug_do_projeto = models.CharField(max_length=255, default="", unique=True)
    nome_do_projeto = models.CharField(max_length=255, default="", unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "projeto"
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.nome_do_projeto


class Arquivo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    file = models.FileField()
    descricao = models.CharField(max_length=255, default="")
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edicao = models.DateTimeField(default=timezone.now)
    extensao = models.CharField(max_length=10, default="")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self) -> str:
        return f"{self.file} | {self.editor} | {self.edicao}"


class Notificacoes(models.Model):
    descricao = models.TextField(default="")
    data = models.DateTimeField(default=timezone.now)
    lida = models.BooleanField(default=False)

    class Meta:
        db_table = "notificacoes"
        verbose_name = "Notificacao"
        verbose_name_plural = "Notificacoes"

    def __str__(self) -> str:
        return f"{self.descricao} | {self.data}"
