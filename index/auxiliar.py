from django import forms

from empresa.models import Login, Notificacoes


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'


def pega_notificacoes(request):
    try:
        login = Login.objects.get(usuario=request.user)
        notificacoes = Notificacoes.objects.filter(empresa=login.empresa)
    except:
        notificacoes = Notificacoes.objects.all()
    return notificacoes
