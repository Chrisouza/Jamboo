import os
import hashlib
from django.conf import settings


def cria_pasta(path):
    os.mkdir(f"{settings.BASE_DIR}/{path}")


def cria_pasta_arquivos(slug, projeto):
    pastas = ["pdf", "imagens", "audios", "videos", "outros"]
    for pasta in pastas:
        os.mkdir(f"media/{slug}/{projeto}/{pasta}")

def gera_hash(text):
    text = f"{text}".encode()
    md5 = hashlib.md5(text)
    return md5.hexdigest()
