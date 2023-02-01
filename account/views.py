import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout

from .forms import FormRegistre, FormLogin, FormFoto, FormSenhaUpdate

from django.contrib.auth.models import User
from .models import Foto

#AREA ADMINISTRATIVA DO USUARIO
def index(request):
    if request.user.is_authenticated:
        foto_perfil = Foto.objects.get(id_usuario=request.user.pk)
        context = { 'foto_perfil':foto_perfil }
        return render(request, 'account/public/home.html', context)
    return redirect("/account/login/")

def configuracoes(request):
    if request.user.is_authenticated:
        old_foto = Foto.objects.get(id_usuario=request.user.pk)
        user = User.objects.get(id=request.user.pk)
        
        form_foto = FormFoto(request.POST, request.FILES, instance=old_foto)
        form_senha_update = FormSenhaUpdate(request.POST, instance=user)

        if request.method == "POST":
            if form_foto.is_valid():
                image_path = old_foto.foto.path.split("/")[:-1]
                image_path = "/".join(image_path)
                image_path = f"{image_path}/usuarios/{old_foto.foto}"
                #print(f"IMAGE_PATH -> {image_path}")
                #if os.path.exists(image_path):
                    #os.remove(image_path)
                form_foto.save()

            if form_senha_update.is_valid():
                user = form_senha_update.save()
                senha = request.POST.get('password')
                user.set_password(senha)
                user.save()

        context = { 'foto_perfil':old_foto, "form_foto":form_foto, "form_senha_update":form_senha_update }
        return render(request, 'account/public/configuracoes.html', context)
    return redirect("/account/login/")

#AREA DE LOGIN / REGISTRE / LOGOUT
def registre(request):
    if not request.user.is_authenticated:
        form_registre = FormRegistre(request.POST or None)
        if request.method == "POST":
            if form_registre.is_valid():
                nome = request.POST.get('nome')
                username = request.POST.get('username')
                email = request.POST.get('email')
                senha = request.POST.get('senha')
                user = User.objects.create_user(first_name=nome, username=username, email=email, password=senha)
                messages.add_message(request, constants.SUCCESS, 'Dados cadastrados com sucesso.')
                Foto(id_usuario=user.pk, foto='usuarios/default.jpg').save()
                return redirect('/account/')
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
                    return redirect('/account/')
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
    return redirect("/")