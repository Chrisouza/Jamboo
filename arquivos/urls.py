from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add-file', views.add_file, name="add-file"),
]
