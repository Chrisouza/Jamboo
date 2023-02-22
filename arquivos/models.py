from django.db import models
from empresa.models import Company
from django.contrib.auth.models import User
from django.utils import timezone


class File(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    file = models.CharField(max_length=255, default="")
    editor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    edition = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "file"
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self) -> str:
        return f"{self.file} | {self.editor} | {self.edition}"
