from django.db import models
from empresa.models import Empresa
from django.contrib.auth.models import User

from django.utils import timezone

class Arquivo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    arquivo = models.CharField(max_length=255, default="")
    editor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    data_edicao = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self) -> str:
        return f'{self.arquivo} | {self.editor} | {self.data_edicao}'