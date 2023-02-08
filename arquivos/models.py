from django.db import models
from empresa.models import Empresa

class Arquivo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    arquivo = models.FileField()
    nome = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self) -> str:
        return self.nome