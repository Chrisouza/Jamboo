from django.db import models

class Login(models.Model):
    user_id = models.IntegerField(default=0)
    empresa = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    def __str__(self) -> str:
        return self.empresa
