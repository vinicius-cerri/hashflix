from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

# LISTA_CATEGORIAS = (
#     ("Armazenar no Banco de Dados", "Aparecer para o Usuário"),
# )

LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTAÇÃO", "Apresentação"),
    ("OUTROS", "Outros")
)

# Criar o Filme
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    qtd_views = models.IntegerField(default=0)
    data_criacao =models.DateTimeField(default=timezone.now)

    # Exibir o Nome do Filme/Curso na Página de Admin (sem isso, ele exibe assim: Filme object (1))
    def __str__(self):
        return self.titulo

# Criar os Episódios
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE) # Cria a relação 1 para
    # muitos com o Filme
    # "Filme": Nome da Tabela que ele vai se relacionar
    # related_name="episodios": serve para descobrir os episódios de determinado filme, vai ser um lista de episódios
    # on_delete=models.CASCADE: faz com que os episódios de um filme que foi excluído, sejam deletados automaticamente
    # Se eu quisesse criar uma relação de muito para muitos, eu deveria usar ManyToManyField ao invés de ForeignKey
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + " - " + self.titulo

# Criar o Usuário
class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")