from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    slug = models.CharField(_('slug'), max_length=255, default="", unique=True)
    name = models.CharField(_('name'), max_length=255, default="", unique=True)
    phone = models.IntegerField(_('phone'), default=0, unique=True)
    created = models.DateTimeField(_('created'), default=timezone.now)
    active = models.BooleanField(_('active'), default=True)

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "companies"
        ordering = ["-id"]

    def __str__(self):
        return self.name
