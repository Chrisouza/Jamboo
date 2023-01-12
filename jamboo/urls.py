from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('usuarios/', include('usuarios.urls')),
    path('arquivos/', include('arquivos.urls')),
    path('painel/', admin.site.urls),
]
