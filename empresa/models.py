from django.db import models

# Create your models here.
class Empresa(models.Model):
    id_adm = models.IntegerField()
    nome = models.CharField(max_length=100, default="", unique=True)
    telefone = models.CharField(max_length=100, default="", unique=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    
    def __str__(self):
        return self.nome
