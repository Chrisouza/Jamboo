import os
from django.conf import settings

def cria_pasta(path):
    os.mkdir(f"{settings.BASE_DIR}/{path}")