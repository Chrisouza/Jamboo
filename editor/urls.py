from django.urls import path
from . import views

urlpatterns = [
    path("<int:projeto>/", views.index),
]
