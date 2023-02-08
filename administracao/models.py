from django.db import models
from django.contrib.auth.models import User
from empresa.models import Empresa

class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

