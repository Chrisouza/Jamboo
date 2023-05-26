import os
import hashlib
import datetime as dt
import uuid
from django.conf import settings


##################################################################
############################ GERAL ###############################
##################################################################
def cria_data():
    hoje = dt.datetime.now()
    return hoje


def gera_hash(text):
    text = f"{text}".encode()
    md5 = hashlib.md5(text)
    return md5.hexdigest()


def cria_nome_da_pasta():
    data = cria_data()
    nome = gera_hash(text=data)
    return nome


def cria_pasta(path):
    os.mkdir(f"{settings.BASE_DIR}/{path}")


def cria_pasta_arquivos(pasta, projeto):
    pastas = ["pdf", "imagens", "audios", "videos", "outros"]
    for folder in pastas:
        os.mkdir(f"media/{pasta}/{projeto}/{folder}")


##################################################################
############################ ARQUIVOS ############################
##################################################################

def apaga_arquivo(path):
    path = f"{settings.BASE_DIR}{path}"
    print(path)
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


def upload_function(arquivo, extensao, pasta, projeto):
    data = f"{cria_data()}".replace(" ","_")
    name_id = uuid.uuid4().hex
    new_name = arquivo.name.replace(" ", "-").lower()
    new_name = f"{data}_{name_id}_{new_name}"

    with open(f"{settings.BASE_DIR}/media/{pasta}/{projeto}/{extensao}/{new_name}", "wb+") as destination:
        for chunk in arquivo.chunks():
            destination.write(chunk)
    return f"/media/{pasta}/{projeto}/{extensao}/{new_name}"


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
