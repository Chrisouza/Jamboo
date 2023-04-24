import os
from django.conf import settings
import datetime
import uuid


def apaga_arquivo(path):
    path = os.path.join(settings.BASE_DIR, path)
    os.remove(path)


def verifica_tipo_de_arquivo(tipo):
    if (tipo == "pdf"):
        tipo = "pdf"
    elif (tipo == "png" or tipo == "jpg" or tipo == "jpeg"):
        tipo = "imagens"
    elif (tipo == "wma" or tipo == "mp3"):
        tipo = "audios"
    elif (tipo == "mp4" or tipo == "wmv"):
        tipo = "videos"
    else:
        tipo = "outros"
    return tipo


def cria_data():
    hoje = datetime.datetime.now()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year
    return f"{dia}-{mes}-{ano}"


def upload_function(arquivo, extensao, slug, projeto):
    data = cria_data()

    name_id = uuid.uuid4().hex
    new_name = arquivo.name.replace(" ", "-").lower()
    new_name = f"{data}_{name_id}_{new_name}"
    
    with open(f"{settings.BASE_DIR}/media/{slug}/{projeto}/{extensao}/{new_name}", "wb+") as destination:
        for chunk in arquivo.chunks():
            destination.write(chunk)
    return f"/media/{slug}/{projeto}/{extensao}/{new_name}"


def read_files(slug):
    paths = []
    files = [{folder: []} for folder in settings.FOLDERS]
    for folder in settings.FOLDERS:
        paths.append(os.path.join(
            settings.BASE_DIR, f"media/{slug}/{folder}/"))
    for x in range(len(paths)):
        key = paths[x].split("/")[-2]
        for _, _, arquivo in os.walk(paths[x]):
            for arq in arquivo:
                files[x][key].append(arq)
    return files
