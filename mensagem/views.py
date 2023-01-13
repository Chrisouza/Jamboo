from django.shortcuts import render
from django.contrib import messages

def mensagem(request, msg):
    if msg == 'admin-cadastrado':
        messages.success(request, "CADASTRADO DE ADMINISTRADOR REALIZADO COM SUCESSO!")
    messages.success(request, "CADASTRADO DE ADMINISTRADOR REALIZADO COM SUCESSO!")
    return render(request, 'mensagem/public/msg.html')