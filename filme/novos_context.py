# Views que estarão disponíveis para todas as páginas
from .models import Filme

def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8] # Ordena os Filmes em Ordem Decrescente
    # [0:8]: Limita a quantidade de filmes na lista para 8 filmes
    return {"lista_filmes_recentes": lista_filmes}

def lista_filmes_em_alta(request):
    lista_filmes = Filme.objects.all().order_by('-qtd_views')[0:8]
    return {"lista_filmes_em_alta": lista_filmes}

def filme_destaque(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    if lista_filmes:
        filme = lista_filmes[0]
    else:
        filme = None
    return {"filme_destaque": filme}