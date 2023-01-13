from django.db import models
from usuario.models import Usuario

class Administrador(Usuario):
    adm = models.BooleanField(default=True)

    def __init__(self):
        super().__init__()
    
    class Meta:
        db_table = "administrador"
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self) -> str:
        return self.nome
