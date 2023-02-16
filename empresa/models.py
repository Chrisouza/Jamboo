from django.db import models
from django.utils import timezone

class Empresa(models.Model):
    slug = models.CharField(max_length=255, default="", unique=True)
    nome = models.CharField(max_length=255, default="", unique=True)
    telefone = models.IntegerField(default="", unique=True)
    criada = models.DateTimeField(default=timezone.now)
    ativa = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["-id"]

    def __str__(self):
        return self.nome