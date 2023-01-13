from django.db import models

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, default="")
    contatos = models.CharField(max_length=255, default="")

    def __str__(self) -> str:
        return self.nome