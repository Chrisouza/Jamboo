from django.db import models

class Cargo(models.Model):
    nome = models.CharField(max_length=100, default="", unique=True)

    class Meta:
        db_table = "cargo"
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
    
    def __str__(self):
        return self.nome

# Create your models here.
class Empresa(models.Model):
    id_adm = models.IntegerField()
    slug = models.CharField(max_length=255, default="", unique=True)
    nome = models.CharField(max_length=255, default="", unique=True)
    telefone = models.CharField(max_length=100, default="", unique=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    
    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    id_empresa = models.IntegerField()
    id_user = models.IntegerField()
    nome = models.CharField(max_length=100, default="", unique=True)
    cargo = models.CharField(max_length=100, default="", unique=True)

    class Meta:
        db_table = "funcionario"
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
    
    def __str__(self):
        return f"{self.nome} | {self.cargo}"

