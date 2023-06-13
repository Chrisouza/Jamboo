import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from empresa.models import Login, Empresa, Nivel, Notificacoes
from django.contrib.auth.models import User
from index.forms import FormEditarEmpresaAdmin, FormEditarEmpresaRoot, FormNovaEmpresa
from index.funcoes import cria_pasta, gera_hash, cria_nome_da_pasta
from django.contrib import messages


def pega_notificacoes():
    notificacoes = Notificacoes.objects.all()
    return notificacoes


def aviso():
    nl = 0
    aviso = False
    for n in pega_notificacoes():
        if not n.visto:
            nl += 1
    if nl > 0:
        aviso = True
    return aviso

# SO ACESSA ESSA INDEX SE NAO FOR SUPER USUARIo


def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        notificacoes = pega_notificacoes()
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)
        context = {"empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "empresa/public/home.html", context)
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def nova_empresa(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notificacoes = pega_notificacoes()
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
                        descricao=f"Nova empresa: '{emp.nome_da_empresa}' cadastrada por: {request.user}!")
                    Notificacoes.objects.create(
                        descricao=f"Usuario '{user.username}' com nivel '{login.nivel.nome_do_nivel}' criado por '{request.user}' para a empresa '{emp.nome_da_empresa}'!")
                    messages.add_message(request, messages.SUCCESS,
                                         "Empresa criada com sucesso!")
                    # messages.add_message(request, messages.INFO, "Um e-mail foi enviado para o administrador!")
                return redirect("/administracao/")
        context = {"form": form,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "empresa/public/nova-empresa.html", context)
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
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
                    descricao=f"Empresa `{empresa}` editada por `{request.user}`!")
                messages.add_message(
                    request, messages.SUCCESS, "Empresa editada com sucesso!")
        else:
            form = FormEditarEmpresaAdmin(instance=empresa)
            if request.method == "POST":
                form = FormEditarEmpresaAdmin(request.POST, instance=empresa)
                form.save()
                Notificacoes.objects.create(
                    descricao=f"Empresa `{empresa}` editada por `{request.user}`!")
                messages.add_message(
                    request, messages.SUCCESS, "Empresa editada com sucesso!")

        notificacoes = pega_notificacoes()
        context = {"form": form, "empresa": empresa,
                   "notificacoes": notificacoes, "aviso": aviso()}
        return render(request, "empresa/public/editar-empresa.html", context)
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
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
            descricao=f"Empresa `{emp}` excluida por `{request.user}`!")
        emp.delete()
        return redirect("/administracao/")
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")

##########################################################
############# ATIVAR/DESATIVAR EMPRESA ###################
##########################################################


def ativar(request, id, acao):
    if request.user.is_authenticated and request.user.is_superuser:
        if acao == "ativar":
            empresa = Empresa.objects.filter(id=id)
            empresa.update(ativo=True)
            Notificacoes.objects.create(
                descricao=f"Empresa `{empresa[0].nome_da_empresa}` foi ativada por `{request.user}`!")
        elif acao == "desativar":
            empresa = Empresa.objects.filter(id=id)
            empresa.update(ativo=False)
            Notificacoes.objects.create(
                descricao=f"Empresa `{empresa[0].nome_da_empresa}` foi desativada por `{request.user}`!")
        else:
            return redirect("/")
    return redirect("/")
