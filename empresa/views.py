import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from empresa.models import Login, Empresa, Nivel
from django.contrib.auth.models import User
from .forms import FormNovaEmpresa
from .funcoes import cria_pasta
from django.contrib import messages

# SO ACESSA ESSA INDEX SE NAO FOR SUPER USUARIO


def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        usuario = Login.objects.get(usuario=request.user)
        empresa = Empresa.objects.get(id=usuario.empresa.id)
        context = {"empresa": empresa}
        return render(request, "empresa/public/home.html", context)
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def nova_empresa(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = FormNovaEmpresa(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                cnpj = request.POST.get("cnpj")
                nome_da_empresa = request.POST.get("nome_da_empresa")
                nome_do_responsavel = request.POST.get("nome_do_responsavel")
                slug_da_empresa = nome_da_empresa.replace(" ", "-")
                telefone = request.POST.get("telefone")

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
                    telefone=telefone
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
                    cria_pasta(f"media/{slug_da_empresa}")
                messages.add_message(request, messages.SUCCESS,
                                     "Empresa criada com sucesso!")
                # messages.add_message(request, messages.INFO, "Um e-mail foi enviado para o administrador!")
                return redirect("/administracao/")
        context = {"form": form}
        return render(request, "empresa/public/nova-empresa.html", context)
    messages.add_message(request, messages.WARNING,
                         "Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")


def editar_empresa(request, id):
    if request.user.is_authenticated:
        try:
            nivel = Login.objects.get(usuario=request.user.id)
        except:
            pass
        if request.user.is_superuser or nivel.nivel.id == 1:
            if request.method == "POST":
                nome_do_responsavel = request.POST.get("nome_do_responsavel")
                telefone = request.POST.get("telefone")
                dados = Empresa.objects.filter(id=id)
                dados.update(
                    nome_do_responsavel=nome_do_responsavel,
                    telefone=telefone
                )
                messages.add_message(request, messages.SUCCESS,
                                     "Dados atualizados com sucesso!")
            empresa = Empresa.objects.get(id=id)
            context = {
                "empresa": empresa
            }
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
        shutil.rmtree(f"{settings.BASE_DIR}/media/{emp.slug_da_empresa}",
                      ignore_errors=True)
        emp.delete()
        return redirect("/administracao/")
    messages.add_message(request, messages.WARNING,
                             "Voce nao tem permissao para acessar essa pagina!")
    return redirect("/")
