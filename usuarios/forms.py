from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    #foto = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password':forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)