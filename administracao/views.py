import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from empresa.models import Backups, Login, Nivel, Empresa, Notificacoes, Projeto, Arquivo
from index.funcoes import cria_data, cria_pasta, cria_pasta_arquivos, cria_zip, paginacao, verifica_tipo_de_arquivo, upload_function, apaga_arquivo
from django.contrib.auth.models import User
from index.forms import FormEditarUsuario, FormNovoArquivo, FormNovoNivel, FormNovoUsuario, FormNovoProjeto
from index.mensagens import *
from index.verificacoes import *


def pega_notificacoes(empresa=None):
    if empresa:
        notificacoes = Notificacoes.objects.filter(empresa=empresa)
    else:
        notificacoes = Notificacoes.objects.all()
    return notificacoes


def update_notificacoes(notificacoes):
    for n in notificacoes:
        up = Notificacoes.objects.filter(id=n.id)
        up.update(visto=1)


def aviso():
    nl = 0
    aviso = False
    for n in pega_notificacoes():
        if not n.visto:
            nl += 1
    if nl > 0:
        aviso = True
    return aviso


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        empresas = Empresa.objects.all()
        notificacoes = pega_notificacoes()
        context = {"empresas": empresas,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/home.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def notificacoes(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            notificacoes = pega_notificacoes()
        else:
            empresa = Login.objects.get(usuario=request.user)
            notificacoes = pega_notificacoes(empresa=empresa)
        if request.method == "POST":
            if request.POST.get("pesquisa"):
                notificacoes = notificacoes.filter(
                    descricao__contains=request.POST.get("pesquisa"))
            if request.POST.get("ordem") == '2':
                notificacoes = notificacoes.order_by("id")

        pages = paginacao(request, data=notificacoes, qtd_pagina=10)

        update_notificacoes(notificacoes)
        context = {"notificacoes": notificacoes, "pages": pages}
        return render(request, "administracao/public/notificacoes.html", context)
    return redirect("/")


##########################################################
############## GERENCIAMENTO DE NIVEIS ###################
##########################################################


def gerenciar_niveis(request):
    if request.user.is_authenticated and request.user.is_superuser:
        niveis = Nivel.objects.all()
        notificacoes = pega_notificacoes()
        context = {"niveis": niveis,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/gerenciar-niveis.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
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
                sucesso(request, msg="N&iacute;vel cadastrado com sucesso!")
                Notificacoes.objects.create(
                    descricao=f"N&iacute;vel '{nivel}' de acesso adicionado por '{request.user}'!")
                return redirect(f"/administracao/niveis/")
        context = {"form": form,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/novo-nivel.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def excluir_nivel(request, nivel):
    if request.user.is_authenticated and request.user.is_superuser:
        nivel = Nivel.objects.get(id=nivel)
        try:
            sucesso(request, msg="N&iacute;vel removido com sucesso!")
            Notificacoes.objects.create(
                descricao=f"N&iacute;vel '{nivel.nome_do_nivel}' de acesso removido por '{request.user}'!")
            nivel.delete()
        except:
            warning(
                request, msg="Não pode apagar esse nivel, pois existe usuários nele!")
            Notificacoes.objects.create(
                descricao=f"Erro ao remover '{nivel.nome_do_nivel}' de n&iacute;vel de acesso '{request.user}'!")
        return redirect(f"/administracao/niveis/")
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect(f"/")

##########################################################
############## GERENCIAMENTO DE USUARIOS #################
##########################################################


def gerenciar_usuarios(request, slug_da_empresa):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        notificacoes = pega_notificacoes()
        logins = Login.objects.filter(
            empresa=Empresa.objects.get(slug_da_empresa=slug_da_empresa).id)
        context = {"slug_da_empresa": slug_da_empresa, "logins": logins,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/gerenciar-usuario.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def novo_usuario(request, slug_da_empresa):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
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

                Notificacoes.objects.create(
                    descricao=f"Usuário '{user}' com n&iacute;vel '{nivel}' criado por '{request.user}' para a empresa '{emp}'!", empresa=emp)

                sucesso(request, msg="Usuario cadastrado com sucesso!")
                return redirect(f"/administracao/usuarios/{slug_da_empresa}/")
        context = {"form": form, "slug_da_empresa": slug_da_empresa,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/novo-usuario.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def editar_usuario(request, slug_da_empresa, usuario):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        notificacoes = pega_notificacoes()
        usuario = User.objects.get(id=usuario)
        form = FormEditarUsuario(instance=usuario)
        if request.method == "POST":
            if request.POST.get("nova_senha") != "":
                usuario.set_password(request.POST.get("nova_senha"))
                usuario.save()
                Notificacoes.objects.create(
                    descricao=f"Usuario '{usuario}' alterou sua senha!")
                info(request, msg="Senha alterado com sucesso!")
        context = {"form": form, "slug_da_empresa": slug_da_empresa,
                   "usuario": usuario, "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/editar-usuario.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def remove_usuario(request, slug_da_empresa, usuario):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        user = User.objects.get(id=usuario)
        login = Login.objects.get(usuario=usuario)
        sucesso(request, msg="Usuario removido com sucesso!")
        Notificacoes.objects.create(
            descricao=f"Usuário:'{login.usuario.username}' de n&iacute;vel: '{login.nivel}' da empresa '{login.empresa.nome_da_empresa}' removido por '{request.user}' !", empresa=login.empresa)
        user.delete()
        return redirect(f"/administracao/usuarios/{slug_da_empresa}/")
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect(f"/")

##########################################################
############# GERENCIAMENTO DE PROJETOS ##################
##########################################################


def gerenciar_projetos(request, slug_da_empresa):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        notificacoes = pega_notificacoes()
        projetos = Projeto.objects.filter(
            empresa=Empresa.objects.get(slug_da_empresa=slug_da_empresa).id)
        try:
            ultimo_bkp = Backups.objects.filter(
                empresa=projetos[0].empresa)[0]
        except:
            ultimo_bkp = None
        context = {"slug_da_empresa": slug_da_empresa, "projetos": projetos, "ultimo_bkp": ultimo_bkp,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/gerenciar-projetos.html", context)
    return redirect("/")


def novo_projeto(request, slug_da_empresa):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        notificacoes = pega_notificacoes()
        form = FormNovoProjeto(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                nome_do_projeto = request.POST.get("nome_do_projeto")
                slug_do_projeto = nome_do_projeto.replace(" ", "-")
                emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)
                Projeto.objects.create(
                    slug_do_projeto=slug_do_projeto, nome_do_projeto=nome_do_projeto, empresa=emp)
                cria_pasta(f"media/{emp.pasta}/{slug_do_projeto}")
                cria_pasta_arquivos(
                    pasta=emp.pasta, projeto=slug_do_projeto)
                sucesso(request, msg="Projeto cadastrado com sucesso!")
                Notificacoes.objects.create(
                    descricao=f"Projeto:'{nome_do_projeto}' da empresa '{emp}' criado por '{request.user}' !")
                return redirect(f"/administracao/projetos/{slug_da_empresa}/")
        context = {"form": form, "slug_da_empresa": slug_da_empresa,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/novo-projeto.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def remove_projeto(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        permissao = permissoes(request, slug_da_empresa)
        if permissao == False:
            return redirect("/")
        projeto = Projeto.objects.get(id=projeto)
        emp = Empresa.objects.get(id=projeto.empresa.id)
        shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.pasta}/{projeto.slug_do_projeto}",
                      ignore_errors=True)
        sucesso(request, msg="Projeto deletado com sucesso!")
        Notificacoes.objects.create(
            descricao=f"Projeto:'{projeto.nome_do_projeto}' da empresa '{emp}' removido por '{request.user}' !")
        projeto.delete()
        return redirect(f"/administracao/projetos/{slug_da_empresa}/")
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def limpa_bkps(request, slug_da_empresa, projeto):
    bkps = Backups.objects.filter(projeto=projeto).order_by("-data")
    for i in range(len(bkps) - 1):
        i += 1
        bkps[i].delete()
    info(request, msg="Apenas o backup mais recente esta disponivel!")
    return redirect(f"/administracao/projetos/{slug_da_empresa}/")


def realizar_bkp(request, slug_da_empresa, projeto):
    data = cria_data()
    data = str(data).replace(" ", "_")
    data = data.replace(":", "_")
    data = data.replace(".", "_")
    data = data.replace("-", "_")
    emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)
    projeto = Projeto.objects.get(id=projeto)

    path_save = f"{settings.BASE_DIR}{settings.MEDIA_URL}{emp.pasta}/{projeto.slug_do_projeto}"
    output_name = f"{emp.slug_da_empresa}_{projeto.nome_do_projeto}_{data}"

    cria_zip(path=path_save, output_name=output_name)
    Backups.objects.create(
        empresa=emp,
        usuario=request.user,
        projeto=projeto
    )
    Notificacoes.objects.create(
        descricao=f"BKP do Projeto:'{projeto.nome_do_projeto}' da empresa '{emp}' criado por '{request.user}' !")

    url = f"{settings.MEDIA_URL}{emp.pasta}/{projeto.slug_do_projeto}/bkps/{output_name}.zip"
    sucesso(
        request, msg=f"BKP do Projeto criado <a href='{url}' download>BAIXAR AGORA</a>!")
    return redirect(f"/administracao/projetos/{slug_da_empresa}/")


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
                   "arquivos": arquivos, "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/gerenciar-arquivos.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def novo_arquivo(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        form = FormNovoArquivo(request.FILES)
        if request.method == "POST":
            emp = Empresa.objects.get(slug_da_empresa=slug_da_empresa)
            files = request.FILES.getlist('file')
            descricao = request.POST.get('descricao')
            editor = request.user

            for file in files:
                extensao = file.name.split(".")[-1]
                extensao = verifica_tipo_de_arquivo(extensao)
                if not extensao:
                    warning(
                        request, msg="Algum arquivo esta fora da extensão permitida!")
                    return redirect(f"/administracao/arquivos/{slug_da_empresa}/{projeto}/novo/")

            for file in files:
                extensao = file.name.split(".")[-1]
                extensao = verifica_tipo_de_arquivo(extensao)
                path = upload_function(
                    arquivo=file, extensao=extensao, pasta=emp.pasta, projeto=projeto)
                projeto = Projeto.objects.get(slug_do_projeto=projeto)
                Arquivo.objects.create(empresa=emp, file=path, descricao=descricao,
                                       editor=editor, extensao=extensao, projeto=projeto)
                Notificacoes.objects.create(
                    descricao=f"Arquivo:'{file}' adicioando ao projeto: '{projeto}' da empresa '{emp}' por '{request.user}' !")
            sucesso(request, msg="Arquivo cadastrado com sucesso!")
            return redirect(f"/administracao/arquivos/{slug_da_empresa}/")

        context = {"form": form, "slug_da_empresa": slug_da_empresa,
                   "projeto": projeto, "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/novo-arquivo.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def ver_arquivos(request, slug_da_empresa, projeto):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes()
        projeto = Projeto.objects.get(slug_do_projeto=projeto)
        arquivos = Arquivo.objects.filter(projeto=projeto.id)
        context = {"slug_da_empresa": slug_da_empresa, "arquivos": arquivos,
                   "projeto": projeto, "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "administracao/public/ver-arquivos.html", context)
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect("/")


def excluir_arquivo(request, slug_da_empresa, projeto, id_file):
    if request.user.is_authenticated:
        arq = Arquivo.objects.get(id=id_file)
        if arq is not None:
            nome_arquivo = f"{arq.file}".split("/")[-1]
            nome_arquivo = f"{nome_arquivo}".split("_")[-1]
            apaga_arquivo(path=f"{arq.file}")
            sucesso(request, msg="Arquivo apagado com sucesso!")
            Notificacoes.objects.create(
                descricao=f"Arquivo:'{nome_arquivo}' do projeto: '{arq.projeto.nome_do_projeto}' por: '{request.user}' !")
            arq.delete()
            return redirect(f"/administracao/arquivos/{slug_da_empresa}/{projeto}/ver/")
    info(request, msg="Você não tem permissão para acessar essa página!")
    return redirect(f"/")
