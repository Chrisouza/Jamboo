from django.contrib import admin
from .models import Empresa, Nivel, Login, Tarefas, TipoEvento

admin.site.register(Empresa)
admin.site.register(Nivel)
admin.site.register(Login)
admin.site.register(TipoEvento)
admin.site.register(Tarefas)
