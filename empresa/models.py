from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Empresa(models.Model):
    slug = models.CharField(max_length=255, default="", unique=True)
    nome = models.CharField(max_length=255, default="", unique=True)
    telefone = models.IntegerField(default="", unique=True)
    criado = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome


class Nivel(models.Model):
    nivel = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "nivel"
        verbose_name = "Nivel"
        verbose_name_plural = "Niveis"

    def __str__(self) -> str:
        return self.nivel


class Login(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    def __str__(self):
        return f"{self.usuario.username}"


class Projeto(models.Model):
    slug = models.CharField(max_length=255, default="", unique=True)
    nome = models.CharField(max_length=255, default="", unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "projeto"
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return f"{self.nome}"


class Arquivo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    file = models.CharField(max_length=255, default="")
    editor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    edicao = models.DateTimeField(default=timezone.now)
    extensao = models.CharField(max_length=10, default="")

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self) -> str:
        return f"{self.file} | {self.editor} | {self.edicao}"