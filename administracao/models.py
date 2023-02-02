from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone
from django.contrib.auth.models import User

class Empresa(models.Model):
    slug = models.CharField(max_length=255, default="", unique=True)
    nome = models.CharField(max_length=255, default="", unique=True)
    telefone = models.CharField(max_length=15, default="", unique=True, help_text="Apenas números")
    data_criada = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome


class Login(models.Model):
    user_id = models.IntegerField(default=0)
    enterprise = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"
