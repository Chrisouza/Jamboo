from django.db import models

class Arquivo(models.Model):
    empresa_id = models.IntegerField()
    arquivo = models.FileField()
    nome = models.CharField(max_length=100, default="")
    tipo = models.CharField(max_length=5, default="")

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self) -> str:
        return self.nome