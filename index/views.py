from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from .forms import FormLogin


def index(request):
    return render(request, "index/public/home.html")

def entrar(request):
    form_login = FormLogin(request.POST or None)
    if request.method == "POST":
        if form_login.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            auth = authenticate(username=username, password=password)
            if auth is not None:
                login(request, auth)
                if auth.is_superuser:
                    return redirect("/administracao/")
                else:
                    return redirect("/empresa/")
                        
    context = {
        'form_login':form_login
    }
    return render(request, "index/public/login.html", context)

def sair(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")