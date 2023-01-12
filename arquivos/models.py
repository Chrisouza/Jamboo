from django.utils import timezone
from django.db import models

class Arquivo(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(default="", blank=True)
    nome = models.CharField(max_length=150)
    path_salvo = models.CharField(max_length=255)
    ultima_edicao = models.DateTimeField(default=timezone.now)
    ultimo_editor = models.PositiveIntegerField(default="")
    nome_editor = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.nome} | {self.nome_editor} | {self.ultima_edicao}"