from django.db import models

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
    