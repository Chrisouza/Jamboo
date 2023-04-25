import shutil
from django.conf import settings

from django.shortcuts import render, redirect
from empresa.models import Login, Nivel, Empresa, Projeto, Arquivo
from empresa.funcoes import cria_pasta, cria_pasta_arquivos
from arquivos.funcoes import verifica_tipo_de_arquivo, upload_function, apaga_arquivo
from django.contrib.auth.models import User
from .forms import FormNovoArquivo, FormNovoUsuario, FormNovoProjeto


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        context = {"empresas": empresas}
        return render(request, "administracao/public/home.html", context)
    return redirect("/")

##########################################################
############## GERENCIAMENTO DE USUARIOS #################
##########################################################


def gerenciar_usuarios(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(
            empresa=Empresa.objects.get(slug=slug).id)
        context = {"slug": slug, "logins": logins}
        return render(request, "administracao/public/gerenciar-usuario.html", context)
    return redirect("/")


def novo_usuario(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoUsuario(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                usuario = request.POST.get("usuario")
                senha = request.POST.get("senha")
                nivel = request.POST.get("nivel")
                user = User.objects.create_user(
                    username=usuario, password=senha, email="")
                emp = Empresa.objects.get(slug=slug)
                nivel = Nivel.objects.get(id=nivel)
                Login.objects.create(usuario=user, empresa=emp, nivel=nivel)
                return redirect(f"/administracao/usuarios/{slug}/")
        context = {"form": form, "slug": slug}
        return render(request, "administracao/public/novo-usuario.html", context)
    return redirect("/")


def remove_usuario(request, slug, usuario):
    if request.user.is_authenticated and request.user.is_superuser:
        User.objects.get(id=usuario).delete()
        return redirect(f"/administracao/usuarios/{slug}/")

##########################################################
############# GERENCIAMENTO DE PROJETOS ##################
##########################################################


def gerenciar_projetos(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        projetos = Projeto.objects.filter(
            empresa=Empresa.objects.get(slug=slug).id)
        context = {"slug": slug, "projetos": projetos}
        return render(request, "administracao/public/gerenciar-projetos.html", context)
    return redirect("/")


def novo_projeto(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoProjeto(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                nome = request.POST.get("nome")
                slug_projeto = nome.replace(" ", "-")
                emp = Empresa.objects.get(slug=slug)
                Projeto.objects.create(
                    slug=slug_projeto, nome=nome, empresa=emp)
                cria_pasta(f"media/{slug}/{slug_projeto}")
                cria_pasta_arquivos(slug=slug, projeto=slug_projeto)
                return redirect(f"/administracao/projetos/{slug}/")
        context = {"form": form, "slug": slug}
        return render(request, "administracao/public/novo-projeto.html", context)
    return redirect("/")


def remove_projeto(request, slug, projeto):
    if request.user.is_authenticated and request.user.is_superuser:
        projeto = Projeto.objects.get(id=projeto)
        shutil.rmtree(f"{settings.BASE_DIR}/media/{slug}/{projeto.slug}",
                      ignore_errors=True)
        projeto.delete()
        return redirect(f"/administracao/projetos/{slug}/")

##########################################################
############# GERENCIAMENTO DE ARQUIVOS ##################
##########################################################


def gerenciar_arquivos(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        projetos = Projeto.objects.filter(
            empresa=Empresa.objects.get(slug=slug).id)
        arquivos = Arquivo.objects.all()
        context = {"slug": slug, "projetos": projetos, "arquivos": arquivos}
        return render(request, "administracao/public/gerenciar-arquivos.html", context)
    return redirect("/")


def novo_arquivo(request, slug, projeto):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovoArquivo(request.FILES)
        if request.method == "POST":
            emp = Empresa.objects.get(slug=slug)
            file = request.FILES.get("file")
            editor = request.user
            extensao = file.name.split(".")[-1]
            extensao = verifica_tipo_de_arquivo(extensao)
            path = upload_function(file, extensao, slug, projeto)
            projeto = Projeto.objects.get(slug=projeto)
            Arquivo.objects.create(
                empresa=emp, file=path, editor=editor, extensao=extensao, projeto=projeto)
            return redirect(f"/administracao/arquivos/{slug}/")
        context = {"form": form, "slug": slug, "projeto": projeto}
        return render(request, "administracao/public/novo-arquivo.html", context)
    return redirect("/")


def excluir_arquivo(request, id_emp, nome_arquivo):
    if request.user.is_authenticated:
        emp = Empresa.objects.get(id=id_emp)
        arq = Arquivo.objects.filter(
            file__contains=nome_arquivo,
            empresa=id_emp
        )
        slug = arq[0].file.split("/")[-2]
        if arq is not None:
            apaga_arquivo(path=f"media/{emp.slug}/{slug}/{nome_arquivo}")
            arq.delete()
    return redirect(f"/arquivos/{id_emp}/")
