from django.contrib import messages
from django.utils.safestring import mark_safe


# SUCCESS - VERDE
def sucesso(request, msg):
    messages.add_message(request, messages.SUCCESS, mark_safe(msg))


# WARNING - VERMELHO
def warning(request, msg):
    messages.add_message(request, messages.WARNING, mark_safe(msg))


# INFO - AZUL
def info(request, msg):
    messages.add_message(request, messages.INFO, mark_safe(msg))
