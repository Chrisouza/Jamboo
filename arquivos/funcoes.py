import os
from django.conf import settings

def apaga_arquivo(path):
    path = os.path.join(settings.BASE_DIR, path)
    os.remove(path)

def verifica_tipo_de_arquivo(tipo):
    if (tipo == "pdf"): tipo = "pdf"
    elif (tipo == "png" or tipo =="jpg" or tipo == "jpeg"): tipo = "imagens"
    elif (tipo == "wma" or tipo == "mp3"): tipo = "audios"
    elif (tipo == "mp4" or tipo == "wmv"): tipo = "videos"
    else: tipo = "outros"
    return tipo

def upload_function(arquivo, slug, tipo):
    new_name = arquivo.name.replace(" ", "_").lower()
    with open(f"{settings.BASE_DIR}/media/{slug}/{tipo}/{new_name}", "wb+") as destination:
        for chunk in arquivo.chunks():
            destination.write(chunk)
    return f"/media/{slug}/{tipo}/{new_name}"

def read_files(slug):
    paths = []
    files = [{folder: []} for folder in settings.FOLDERS]
    for folder in settings.FOLDERS:
        paths.append( os.path.join(settings.BASE_DIR, f"media/{slug}/{folder}/") )
    for x in range(len(paths)):
        key = paths[x].split("/")[-2]
        for _,_,arquivo in os.walk(paths[x]):
            for arq in arquivo:
                files[x][key].append(arq)
    return files
