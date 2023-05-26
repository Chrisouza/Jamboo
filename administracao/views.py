import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from empresa.models import Login, Nivel, Empresa, Notificacoes, Projeto, Arquivo
from index.funcoes import cria_pasta, cria_pasta_arquivos, verifica_tipo_de_arquivo, upload_function, apaga_arquivo
from django.contrib.auth.models import User
from index.forms import FormNovoArquivo, FormNovoNivel, FormNovoUsuario, FormNovoProjeto
from index.mensagens import *


def pega_notificacoes():
    notificacoes = Notificacoes.objects.all()
    return notificacoes


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        notificacoes = pega_notificacoes()
        context = {"empresas": empresas, "notificacoes": notificacoes}
        return render(request, "administracao/public/home.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def notificacoes(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notificacoes = pega_notificacoes()
        context = {"notificacoes": notificacoes}
        return render(request, "administracao/public/notificacoes.html", context)
    return redirect("/")


##########################################################
############## GERENCIAMENTO DE NIVEIS ###################
##########################################################


def gerenciar_niveis(request):
    if request.user.is_authenticated and request.user.is_superuser:
        niveis = Nivel.objects.all()
        notificacoes = pega_notificacoes()
        context = {"niveis": niveis, "notificacoes": notificacoes}
        return render(request, "administracao/public/gerenciar-niveis.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def novo_nivel(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notificacoes = pega_notificacoes()
        form = FormNovoNivel(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                nivel = request.POST.get("nome_do_nivel")
                descricao = request.POST.get("descricao")
                Nivel.objects.create(nome_do_nivel=nivel, descricao=descricao)
                sucesso(request, msg="Nivel cadastrado com sucesso!")
                Notificacoes.objects.create(
                    descricao="Novo nivel de acesso adicionado!")
                return redirect(f"/administracao/niveis/")
        context = {"form": form, "notificacoes": notificacoes}
        return render(request, "administracao/public/novo-nivel.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def excluir_nivel(request, nivel):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            Nivel.objects.get(id=nivel).delete()
            sucesso(request, msg="Nivel removido com sucesso!")
        except:
            warning(
                request, msg="Nao pode apagar esse nivel, pois existe usuarios nele!")
        finally:
            return redirect(f"/administracao/niveis/")
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect(f"/")

##########################################################
############## GERENCIAMENTO DE USUARIOS #################
##########################################################


def gerenciar_usuarios(request, slug_da_empresa):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        logins = Login.objects.filter(
            empresa=Empresa.objects.get(slug_da_empresa=slug_da_empresa).id)
        context = {"slug_da_empresa": slug_da_empresa, "logins": logins,
                   "notificacoes": notificacoes}
        return render(request, "administracao/public/gerenciar-usuario.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def novo_usuario(request, slug_da_empresa):
    if request.user.is_authenticated:
        try:
            nivel = Login.objects.get(usuario=request.user.id)
        except:
            pass
        if request.user.is_superuser or nivel.nivel.id == 1:
            notificacoes = pega_notificacoes()
            form = FormNovoUsuario(request.POST or None)
            if request.method == "POST":
                if form.is_valid():
                    usuario = request.POST.get("usuario")
                    senha = request.POST.get("senha")
                    email = request.POST.get("email")
                    nivel = request.POST.get("nivel")

                    user = User.objects.create_user(
                        username=usuario, password=senha, email=email)
                    emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)

                    nivel = Nivel.objects.get(id=nivel)
                    Login.objects.create(
                        usuario=user, empresa=emp, nivel=nivel)

                    sucesso(request, msg="Usuario cadastrado com sucesso!")
                    return redirect(f"/administracao/usuarios/{slug_da_empresa}/")
            context = {"form": form, "slug_da_empresa": slug_da_empresa,
                       "notificacoes": notificacoes}
            return render(request, "administracao/public/novo-usuario.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def remove_usuario(request, empresa, usuario):
    if request.user.is_authenticated:
        try:
            nivel = Login.objects.get(usuario=request.user.id)
        except:
            pass
        if request.user.is_superuser or nivel.nivel.id == 1:
            User.objects.get(id=usuario).delete()
            sucesso(request, msg="Usuario removido com sucesso!")
            return redirect(f"/administracao/usuarios/{empresa}/")
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect(f"/")

##########################################################
############# GERENCIAMENTO DE PROJETOS ##################
##########################################################


def gerenciar_projetos(request, slug_da_empresa):
    if request.user.is_authenticated:
        try:
            login = Login.objects.get(usuario=request.user.id)
        except:
            pass
        if request.user.is_superuser or login.nivel.id == 1:
            notificacoes = pega_notificacoes()
            projetos = Projeto.objects.filter(
                empresa=Empresa.objects.get(slug_da_empresa=slug_da_empresa).id)
            context = {"slug_da_empresa": slug_da_empresa, "projetos": projetos,
                       "notificacoes": notificacoes}
            return render(request, "administracao/public/gerenciar-projetos.html", context)
    return redirect("/")


def novo_projeto(request, slug_da_empresa):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            notificacoes = pega_notificacoes()
            form = FormNovoProjeto(request.POST or None)
            if request.method == "POST":
                if form.is_valid():
                    nome_do_projeto = request.POST.get("nome_do_projeto")
                    slug_do_projeto = nome_do_projeto.replace(" ", "-")
                    emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)
                    Projeto.objects.create(slug_do_projeto=slug_do_projeto, nome_do_projeto=nome_do_projeto, empresa=emp)
                    cria_pasta(f"media/{emp.pasta}/{slug_do_projeto}")
                    cria_pasta_arquivos(pasta=emp.pasta, projeto=slug_do_projeto)
                    sucesso(request, msg="Projeto cadastrado com sucesso!")
                    return redirect(f"/administracao/projetos/{slug_da_empresa}/")
            context = {"form": form, "slug_da_empresa": slug_da_empresa,
                       "notificacoes": notificacoes}
            return render(request, "administracao/public/novo-projeto.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def remove_projeto(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            projeto = Projeto.objects.get(id=projeto)
            emp = Empresa.objects.get(id=projeto.empresa.id)
            shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.pasta}/{projeto.slug_do_projeto}",
                          ignore_errors=True)
            projeto.delete()
            sucesso(request, msg="Projeto deletado com sucesso!")
            return redirect(f"/administracao/projetos/{slug_da_empresa}/")
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")

##########################################################
############# GERENCIAMENTO DE ARQUIVOS ##################
##########################################################


def gerenciar_arquivos(request, slug_da_empresa):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        projetos = Projeto.objects.filter(
            empresa=Empresa.objects.get(slug_da_empresa=slug_da_empresa).id)
        arquivos = Arquivo.objects.all().order_by("-id")
        context = {"slug_da_empresa": slug_da_empresa, "projetos": projetos,
                   "arquivos": arquivos, "notificacoes": notificacoes}
        return render(request, "administracao/public/gerenciar-arquivos.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def novo_arquivo(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        form = FormNovoArquivo(request.FILES)
        if request.method == "POST":
            emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)
            file = request.FILES.get("file")
            descricao = request.POST.get('descricao')
            editor = request.user
            extensao = file.name.split(".")[-1]
            extensao = verifica_tipo_de_arquivo(extensao)
            path = upload_function(arquivo=file, extensao=extensao, pasta=emp.pasta, projeto=projeto)
            projeto = Projeto.objects.get(slug_do_projeto=projeto)
            Arquivo.objects.create(
                empresa=emp, file=path, descricao=descricao, editor=editor, extensao=extensao, projeto=projeto)
            sucesso(request, msg="Arquivo cadastrado com sucesso!")
            return redirect(f"/administracao/arquivos/{slug_da_empresa}/")
        context = {"form": form, "slug_da_empresa": slug_da_empresa,
                   "projeto": projeto, "notificacoes": notificacoes}
        return render(request, "administracao/public/novo-arquivo.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def ver_arquivos(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        projeto = Projeto.objects.get(slug_do_projeto=projeto)
        arquivos = Arquivo.objects.filter(projeto=projeto.id)
        context = {"slug_da_empresa": slug_da_empresa, "arquivos": arquivos,
                   "projeto": projeto, "notificacoes": notificacoes}
        return render(request, "administracao/public/ver-arquivos.html", context)
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def excluir_arquivo(request, slug_da_empresa, projeto, id_file):
    if request.user.is_authenticated:
        arq = Arquivo.objects.get(id=id_file)
        if arq is not None:
            apaga_arquivo(path=f"{arq.file}")
            arq.delete()
            sucesso(request, msg="Arquivo apagado com sucesso!")
            return redirect(f"/administracao/arquivos/{slug_da_empresa}")
    info(request, msg="Voce nao tem permissao para acessar essa pagina!")
    return redirect(f"/")
