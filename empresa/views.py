import shutil

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from empresa.models import Login, Empresa, Nivel, Notificacoes, Tarefas, TipoEvento
from index.forms import FormEditarEmpresaAdmin, FormEditarEmpresaRoot, FormNovaAgenda, FormNovaEmpresa
from index.funcoes import cria_pasta, cria_nome_da_pasta, paginacao
from index.verificacoes import *
from index.auxiliar import pega_notificacoes, aviso

# SO ACESSA ESSA INDEX SE NAO FOR SUPER USUARIO


def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)
        permissao = permissoes(request, empresa.slug_da_empresa)
        if permissao == False:
            return redirect("/")
        notificacoes = pega_notificacoes(request=request)
        tarefas = Tarefas.objects.filter(
            empresa=empresa, inicio_data=timezone.now().date())
        context = {"empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso(request), "tarefas": tarefas}
        return render(request, "empresa/public/home.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")


def nova_empresa(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notificacoes = pega_notificacoes(request=request)
        form = FormNovaEmpresa(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                cnpj = request.POST.get("cnpj")
                nome_da_empresa = request.POST.get("nome_da_empresa")
                slug_da_empresa = f"{nome_da_empresa}".replace(" ", "-")
                nome_do_responsavel = request.POST.get("nome_do_responsavel")
                telefone = request.POST.get("telefone")
                pasta = cria_nome_da_pasta()

                usuario_administrador = request.POST.get("administrador")
                email = request.POST.get("email")
                senha = request.POST.get("senha")

                user = User.objects.create_user(
                    username=usuario_administrador,
                    email=email,
                    password=senha
                )

                emp = Empresa.objects.create(
                    cnpj=cnpj,
                    slug_da_empresa=slug_da_empresa,
                    nome_da_empresa=nome_da_empresa,
                    nome_do_responsavel=nome_do_responsavel,
                    telefone=telefone,
                    pasta=pasta
                )

                login = Login.objects.create(
                    usuario=user,
                    empresa=emp,
                    nivel=Nivel.objects.get(id=1)
                )

                ##################################
                # AREA DO ENVIO DE EMAIL
                ##################################
                # corpo = f"Os dados de login e senha do adminsitradorsoa:"
                # corpo += f"Login: {usuario_administrador} - Senha: {senha}"
                # form.envia_email(destinatario=email, corpo=corpo)

                if emp:
                    cria_pasta(f"media/{pasta}")
                    Notificacoes.objects.create(
                        descricao=f"Nova empresa: '{emp.nome_da_empresa}' cadastrada por: {request.user}!", empresa=emp)
                    Notificacoes.objects.create(
                        descricao=f"Usuário '{user.username}' com nivel '{login.nivel.nome_do_nivel}' criado por '{request.user}' para a empresa '{emp.nome_da_empresa}'!", empresa=emp)
                    messages.add_message(request, messages.SUCCESS,
                                         "Empresa criada com sucesso!")
                    # messages.add_message(request, messages.INFO, "Um e-mail foi enviado para o administrador!")
                return redirect("/administracao/")
        context = {"form": form,
                   "notificacoes": notificacoes, "aviso": aviso(request)}
        return render(request, "empresa/public/nova-empresa.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")


def editar_empresa(request, id):
    if request.user.is_authenticated:
        empresa = Empresa.objects.get(id=id)
        if request.user.is_superuser:
            form = FormEditarEmpresaRoot(instance=empresa)
            if request.method == "POST":
                form = FormEditarEmpresaRoot(request.POST, instance=empresa)
                form.save()
                Notificacoes.objects.create(
                    descricao=f"Empresa `{empresa}` editada por `{request.user}`!", empresa=empresa)
                messages.add_message(
                    request, messages.SUCCESS, "Empresa editada com sucesso!")
        else:
            form = FormEditarEmpresaAdmin(instance=empresa)
            if request.method == "POST":
                form = FormEditarEmpresaAdmin(request.POST, instance=empresa)
                form.save()
                Notificacoes.objects.create(
                    descricao=f"Empresa `{empresa}` editada por `{request.user}`!", empresa=empresa)
                messages.add_message(
                    request, messages.SUCCESS, "Empresa editada com sucesso!")

        notificacoes = pega_notificacoes(request=request)
        context = {"form": form, "empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso(request)}
        return render(request, "empresa/public/editar-empresa.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")


def excluir_empresa(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        logins = Login.objects.filter(empresa=id)
        for login in logins:
            User.objects.get(username=login.usuario.username).delete()
        emp = Empresa.objects.get(id=id)
        try:
            shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.pasta}")
        except:
            pass
        Notificacoes.objects.create(
            descricao=f"Empresa `{emp}` excluida por `{request.user}`!", empresa=emp)
        emp.delete()
        return redirect("/administracao/")
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")

##########################################################
############# ATIVAR/DESATIVAR EMPRESA ###################
##########################################################


def ativar(request, id, acao):
    if request.user.is_authenticated and request.user.is_superuser:
        empresa = Empresa.objects.filter(id=id)
        if acao == "ativar":
            empresa.update(ativo=True)
            Notificacoes.objects.create(
                descricao=f"Empresa `{empresa[0].nome_da_empresa}` foi ativada por `{request.user}`!", empresa=empresa[0])
        elif acao == "desativar":
            empresa.update(ativo=False)
            Notificacoes.objects.create(
                descricao=f"Empresa `{empresa[0].nome_da_empresa}` foi desativada por `{request.user}`!", empresa=empresa[0])
        else:
            return redirect("/")
    return redirect("/")


##########################################################
############# REUNIAO / CALENDARIO EMPRESA ###############
##########################################################

def reuniao(request, tarefa):
    if request.user.is_authenticated:

        notificacoes = pega_notificacoes(request=request)
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)

        room = f"{tarefa} {empresa.nome_da_empresa}"

        context = {"empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso(request), "room": room}
        return render(request, "empresa/public/reuniao.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")


def agenda(request):
    if request.user.is_authenticated:
        notificacoes = pega_notificacoes(request=request)
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)

        tarefas = Tarefas.objects.filter(empresa=empresa)

        pages = paginacao(request, data=tarefas, qtd_pagina=10)

        context = {"empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso(request), 'tarefas': pages}
        return render(request, "empresa/public/agenda.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")


def nova_agenda(request):
    if request.user.is_authenticated:
        form = FormNovaAgenda(request.POST or None)
        notificacoes = pega_notificacoes(request=request)
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)

        if request.method == "POST":
            if form.is_valid():
                titulo = request.POST.get('titulo')
                descricao = request.POST.get('descricao')
                inicio_data = request.POST.get('inicio_data')
                inicio_hora = request.POST.get('inicio_hora')
                fim_data = request.POST.get('fim_data')
                fim_hora = request.POST.get('fim_hora')
                tipo = request.POST.get('tipo')
                tipo = TipoEvento.objects.get(id=tipo)

                Tarefas.objects.create(
                    titulo=titulo,
                    descricao=descricao,
                    inicio_data=inicio_data,
                    inicio_hora=inicio_hora,
                    fim_data=fim_data,
                    fim_hora=fim_hora,
                    empresa=empresa,
                    tipo=tipo
                )
                messages.add_message(
                    request, messages.WARNING, "Tarefa agendada com sucesso!")
                Notificacoes.objects.create(
                    descricao=f"Tarefa adicionada da empresa '{empresa}' por '{request.user}' !", empresa=empresa)
                return redirect("/empresa/")
            else:
                print('nao esta valido')

        context = {"empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso(request), "form": form}
        return render(request, "empresa/public/nova-agenda.html", context)
    messages.add_message(request, messages.WARNING,
                         "Você não tem permissão para acessar essa página!")
    return redirect("/")
