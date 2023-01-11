from django.db import models

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50) #(Prestador de Serviço, Administrador e Engenheiro)

    class Meta:
        db_table = 'perfil'
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self) -> str:
        return self.nome


class Foto(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    foto = models.CharField(max_length=100) #(Prestador de Serviço, Administrador e Engenheiro)

    class Meta:
        db_table = 'foto'
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"

    def __str__(self) -> str:
        return f"{self.id_user}|{self.foto}"