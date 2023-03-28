from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("index.urls")),
    path("administracao/", include("administracao.urls")),
    path("arquivos/", include("arquivos.urls")),
    path("empresa/", include("empresa.urls")),
    path("projetos/", include('projeto.urls')),
    path("painel/", admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
