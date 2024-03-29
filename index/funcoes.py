from django import template
import os
import hashlib
import datetime as dt
import uuid
import shutil


from django.conf import settings
from django.core.paginator import Paginator


def paginacao(request, data, qtd_pagina):
    paginacao = Paginator(data, qtd_pagina)
    page_num = request.GET.get('page')
    page = paginacao.get_page(page_num)
    return page

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
    pastas = ["pdf", "imagens", "videos", "bkps"]
    for folder in pastas:
        os.mkdir(f"media/{pasta}/{projeto}/{folder}")


def cria_zip(path, output_name):
    pastas = ["pdf", "imagens", "videos"]
    os.mkdir(f"{path}/bkps/{output_name}")
    for p in pastas:
        shutil.copytree(f"{path}/{p}/", f"{path}/bkps/{output_name}/{p}/")
    shutil.make_archive(f'{path}/bkps/{output_name}',
                        'zip', './', f"{path}/bkps/{output_name}")
    shutil.rmtree(f"{path}/bkps/{output_name}")

##################################################################
############################ ARQUIVOS ############################
##################################################################


def apaga_arquivo(path):
    path = f"{settings.BASE_DIR}{path}"
    print(path)
    os.remove(path)


def verifica_tipo_de_arquivo(tipo):
    imagens = ['tiff', 'jpg', 'jpeg', 'png', 'laz', 'dwg']
    videos = ['mp4', 'wmv']
    pdfs = ['pdf']

    if tipo in imagens:
        tipo = "imagens"
        return tipo
    
    if tipo in videos:
        tipo = "videos"
        return tipo
    
    if tipo in pdfs:
        tipo = 'pdf'
        return tipo
    
    return False


def upload_function(arquivo, extensao, pasta, projeto):
    data = f"{cria_data()}".replace(" ", "_")
    tipo = arquivo.name.split(".")[1]
    name_id = uuid.uuid4().hex
    new_name = f"{data}-{name_id}.{tipo}"
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
