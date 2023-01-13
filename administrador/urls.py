from django.urls import path
from . import views

urlpatterns = [
    path('novo-adm/', views.novo_adm, name='novo-adm'),
]
