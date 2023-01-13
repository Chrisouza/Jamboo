from django.db import models
from django.contrib.auth.hashers import make_password as mp

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, default="")
    email = models.EmailField(max_length=150, default="")
    senha = models.CharField(max_length=150, default="")
    ativo = models.BooleanField(default=True)
    logado = models.BooleanField(default=False)

    def make_password(self, password):
        return mp(password)

    class Meta:
        abstract = True
