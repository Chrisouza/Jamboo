from django.urls import path
from . import views

urlpatterns = [
    path('minhas-empresas/', views.minhas_empresas, name='minhas-empresas'),
    path('nova-empresa/', views.nova_empresa, name='nova-empresa'),
]