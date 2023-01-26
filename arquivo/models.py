from django.db import models
from django.utils import timezone

# Create your models here.
class Arquivo(models.Model):
    id_empresa = models.IntegerField()
    id_editor = models.IntegerField()
    file = models.FileField()
    nome = models.CharField(max_length=255, default="")
    data_edicao = models.DateField(default=timezone.now)
    editando = models.BooleanField(default=False)

    class Meta:
        db_table = "arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

    def __str__(self):
        return self.nome
