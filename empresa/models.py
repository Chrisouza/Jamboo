from django.db import models
from autoslug import AutoSlugField

# Create your models here.
class Empresa(models.Model):
    id_adm = models.IntegerField()
    slug = AutoSlugField(populate_from='nome')
    nome = models.CharField(max_length=100, default="", unique=True)
    telefone = models.CharField(max_length=100, default="", unique=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    
    def __str__(self):
        return self.nome
