from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, default="", unique=True)
    slug_da_empresa = models.CharField(max_length=255, default="", unique=True)
    nome_da_empresa = models.CharField(max_length=255, default="", unique=True)
    nome_do_responsavel = models.CharField(
        max_length=255, default="", unique=True)
    telefone = models.CharField(max_length=16, default="", unique=True)
    pasta = models.CharField(max_length=255, default="")
    criado = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["-id"]

    def __str__(self):
        return self.nome_da_empresa


class Nivel(models.Model):
    nome_do_nivel = models.CharField(max_length=100, default="")
    descricao = models.TextField(max_length=255, default="")
    data_criado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "nivel"
        verbose_name = "Nivel"
        verbose_name_plural = "Niveis"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.nome_do_nivel


class Login(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)
    primeiro_acesso = models.BooleanField(default=False)
    data_criado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.usuario.username}"


class Projeto(models.Model):
    slug_do_projeto = models.CharField(max_length=255, default="", unique=True)
    nome_do_projeto = models.CharField(max_length=255, default="", unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default="")
    data_criado = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "projeto"
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-id"]

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
    data_upload = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.file} | {self.editor} | {self.edicao}"


class Notificacoes(models.Model):
    descricao = models.TextField(default="")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default="")
    visto = models.BooleanField(default=0)
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "notificacoes"
        verbose_name = "Notificacao"
        verbose_name_plural = "Notificacoes"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.descricao} | {self.data}"


class Backups(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "backups"
        verbose_name = "Backup"
        verbose_name_plural = "Backups"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.empresa} | {self.usuario} | {self.data}"


class TipoEvento(models.Model):
    nome = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "tipoevento"
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Eventos"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.nome}"


class Tarefas(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, default="", unique=True)
    descricao = models.TextField()
    inicio_data = models.DateField(default="")
    inicio_hora = models.TimeField(default="")
    fim_data = models.DateField(default="")
    fim_hora = models.TimeField(default="")
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)

    class Meta:
        db_table = "tarefas"
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.titulo
