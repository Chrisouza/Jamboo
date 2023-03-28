from django import forms


class FormNovoArquivo(forms.Form):
    file = forms.FileField()
