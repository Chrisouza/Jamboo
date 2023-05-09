from django.contrib import messages


# SUCCESS - VERDE
def sucesso(request, msg):
    messages.add_message(request, messages.SUCCESS, msg)


# WARNING - VERMELHO
def warning(request, msg):
    messages.add_message(request, messages.WARNING, msg)


# INFO - AZUL
def info(request, msg):
    messages.add_message(request, messages.INFO, msg)
