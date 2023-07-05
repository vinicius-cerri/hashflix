from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class FormHomepage(forms.Form):
    email = forms.EmailField(label=False) # label=False: Serve para não exibir o Texto do Formulário

class CriarContaForm(UserCreationForm):
    email = forms.EmailField() # Por padrão, ao deixar vazio os argumentos, o campo se torna obrigatório

    # Class Meta (serve para dizer qual modelo ele deve usar com referência)
    class Meta:
        model = Usuario
        # Campos que serão Exibidos no Formulário
        fields = ('username', 'email', 'password1', 'password2') # 'password1': Campo Senha
        # 'password2': Campo Confirmação de Senha