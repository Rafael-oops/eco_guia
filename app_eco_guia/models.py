from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

# Mapeamento do banco de dados por meio de classes (a classe é uma tabela, as variáveis da classe são as colunas da tabela)
class USUARIO(models.Model):
    nome = models.CharField(max_length=100) # definindo o max de caracteres como 100
    email = models.EmailField(unique=True) # definindo o campo email como único (não irá permitir o banco de dados registrar emails iguais)
    username = models.CharField(max_length=30, unique=True)
    senha = models.CharField(max_length=8)
    
    # Função que mostra o nome do usuário no admin do django no lugar do 'user.object'
    def __str__(self):
        return self.nome

class RECLAMACOE(models.Model):
    rnome = models.CharField(max_length=100)
    remail = models.EmailField()
    mensagem = models.CharField(max_length=2000)
    id_usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE,related_name='reclamacoes')
    
    def __str__(self):
        return self.rnome
    
    
class CATEGORIA(models.Model):
    nome_categ = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_categ
    
class IDEIA(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.CharField(max_length=6000)
    id_categ = models.ForeignKey(CATEGORIA, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo
        
    
    

#---------------------------------------   Histórico de Imagens   ---------------------------------------#

# Definição das categorias possíveis
CATEGORIES = [
    ("cardboard", "Cardboard"),
    ("glass", "Glass"),
    ("metal", "Metal"),
    ("paper", "Paper"),
    ("plastic", "Plastic"),
    ("trash", "Trash"),
]

# Modelo para armazenar o histórico de imagens classificadas
class ImageHistory(models.Model):
    """
    Modelo que armazena o histórico de imagens classificadas pelo sistema.
    Cada instância guarda uma categoria de resíduo, a contagem de vezes que essa categoria
    foi classificada e a última imagem classificada nessa categoria.
    """
    category = models.CharField(max_length=100, choices=CATEGORIES) # Limita as categorias às opções definidas
    count = models.IntegerField(default=1,validators=[MinValueValidator(1)])  # Valida que o valor deve ser >= 1
    image = models.ImageField(upload_to='history_images/')  # Define o diretório de upload para as imagens
    last_classified = models.DateTimeField(auto_now=True) # Atualiza automaticamente com a data/hora da última classificação

    def __str__(self):
        return self.category # Representação do objeto: retorna o nome da categoria classificada

    class Meta:
        unique_together = ('category', 'image') # Define que a combinação de categoria e imagem deve ser única no banco de dados

        # Define índices para otimizar consultas por categoria e última classificação
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['last_classified']),
        ]
