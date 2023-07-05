from django.shortcuts import render, redirect, reverse
from.models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin # Tem que ser o 1º Argumento da Classe

# Create your views here.
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) # Redireciona o Usuário para a Homepage

    # Redirecionar a Pessoa de maneira Inteligente
    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            # Levar para a Página de Login, caso o usuário tenha uma conta no site
            return reverse('filme:login')
        else:
            # Levar para a Página de Criar Conta, caso o usuário não tenha uma conta no site
            return reverse('filme:criarconta')

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    # Função para contabilizar a Visualização no Filme
    def get(self, request, *args, **kwargs): # Essa Função espera um Redirecionamento (uma Página como resposta)
        filme = self.get_object()
        filme.qtd_views += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super(Detalhesfilme, self).get(request, *args, **kwargs) # Redireciona o Usuário para a URL final

    # View Filmes Relacionados que estará disponível apenas nessa página
    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs) # Para manter a função principal
        # (não sobrescrevê-la, apenas adicionar as próximas linhas de código na função)
        # Filtrar a Tabela de Filmes pegando apenas os itens com a Categoria da Página
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:8]
        context['filmes_relacionados'] = filmes_relacionados
        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    # Função que verifica se o Formulário é Válido (salvar alterações no Banco de Dados, criar uma conta)
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Função para o Formulário bem sucedido (validação der certo)
    def get_success_url(self): # Essa Função espera uma URL (um Link como resposta)
        return reverse('filme:login')