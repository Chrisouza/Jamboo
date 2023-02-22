from django.db import models
from django.contrib.auth.models import User
from empresa.models import Company
from django.utils.translation import gettext_lazy as _


class Level(models.Model):
    level = models.CharField(_("level"), max_length=100, default="")

    class Meta:
        db_table = "level"
        verbose_name = "level"
        verbose_name_plural = "levels"

    def __str__(self) -> str:
        return self.level


class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "login"
        verbose_name = "Login"
        verbose_name_plural = "Logins"

    def __str__(self):
        return f"{self.user.username}"
