from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout

from .forms import FormRegistre, FormLogin

from django.contrib.auth.models import User
from empresa.models import Empresa

def index(request):
    context = {}
    return render(request, 'account/public/home.html', context)

def registre(request):
    if not request.user.is_authenticated:
        form_registre = FormRegistre(request.POST or None)
        if request.method == "POST":
            if form_registre.is_valid():
                empresa = request.POST.get('empresa')
                ver_emp = Empresa.objects.filter(nome=empresa)
                if not ver_emp:
                    nome = request.POST.get('nome')
                    username = request.POST.get('username')
                    email = request.POST.get('email')
                    senha = request.POST.get('senha')
                    user = User.objects.create_user(first_name=nome, username=username, email=email, password=senha)
                    emp = Empresa(adm_id=user.pk, nome=empresa)
                    emp.save()
                    messages.add_message(request, constants.SUCCESS, 'Dados cadastrados com sucesso.')
                    return redirect('/account/')
                else:
                    messages.add_message(request, constants.INFO, 'Essa empresa ja esta cadastrada.')
                    form_registre = FormRegistre(request.POST or None)
        context = {
            'form':form_registre
        }
        return render(request, 'account/public/registre.html', context)
    else:
        return redirect('/account/')

def logar(request):
    if not request.user.is_authenticated:
        form_logar = FormLogin(request.POST or None)
        if request.method == "POST":
            if form_logar.is_valid():
                username = request.POST.get('username')
                senha = request.POST.get('senha')
                auth = authenticate(username=username, password=senha)
                if auth is not None:
                    login(request, auth)
                    messages.add_message(request, constants.INFO, "Login realizado com sucesso")
        context = {
            'form':form_logar
        }
        return render(request, 'account/public/login.html', context)
    else:
        return redirect('/account/')

def deslogar(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, constants.INFO, "Deslogado com sucesso")
    return redirect("/account/")