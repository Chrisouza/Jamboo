from tkinter.ttk import Widget
from django.db import models
from django.forms import PasswordInput

# Create your models here.
class Foto(models.Model):
    id_usuario = models.IntegerField()
    foto = models.ImageField(default="default.png", upload_to="usuarios/")

    class Meta:
        db_table = "foto"
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"
    
    def __str__(self):
        return self.foto.url