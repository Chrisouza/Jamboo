from django.db import models
from django.contrib.auth.models import User
from empresa.models import Empresa

class Nivel(models.Model):
    nivel = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "nivel"
        verbose_name = "Nivel"
        verbose_name_plural = "Niveis"

    def __str__(self) -> str:
        return self.nivel

class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    def __str__(self):
        return f"{self.user.username}"

