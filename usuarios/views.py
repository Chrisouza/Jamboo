from django.shortcuts import render
from .forms import LoginForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('/usuarios/painel/')
    
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = request.POST.get('username') 
            senha = request.POST.get('senha') 
            auth = authenticate(username=username, password=senha)
            if auth is not None:
                login(request, auth)
                return redirect('/usuarios/painel/')
            else:
                pass
    context = {
        'form':form
    }
    return render(request, 'public/login.html', context)

def registre(request):
    if request.user.is_authenticated:
        return redirect('/usuarios/painel/')
    
    form = UserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'public/registre.html', context)

def sair(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/usuarios/')
    return redirect('/usuarios/')
