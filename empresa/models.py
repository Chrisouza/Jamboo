from django.db import models

# Create your models here.
class Empresa(models.Model):
    adm_id = models.IntegerField()
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['-id']
    
    def __str__(self):
        return self.nome
