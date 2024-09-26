from django.shortcuts import render, redirect
from .models import USUARIO # importa o mapeamento do banco de dados do arquivo models.py
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'index.html')

def cadastro(request):
    usuario = USUARIO.objects.all() # Seleciona todas as colunas do banco de dados mapeadas no arquivo models.py (ver linha 6 do models.py) e armazzena na variável usuario
    return render(request, 'cadastro.html', {'usuarios': usuario}) # Renderiza a requisição para a página cadastro.html e dá um apelido usuários para a variável usuário para o cadastro saber de onde ta importando os dados (ver linha 15 do cadastro.html)

def salvar(request):
    n_nome = request.POST.get("nome") # pega o valor do input no formulário com o name="nome" (ver linha 43 do cadastro.html) e armazena na variável n_nome
    n_email = request.POST.get("email")
    n_username = request.POST.get("username")
    n_senha = request.POST.get("senha")
    n_conf = request.POST.get("conf")
    
    # faz a comparação das senhas e envia para a página cadastro.html
    if n_conf == n_senha:
        USUARIO.objects.create(nome = n_nome, email = n_email, username= n_username, senha = n_senha) # registra no banco de dados as informações inseridas no forms
        usuario = USUARIO.objects.all() # seleciona todos os registros da models.py(na tabela  Usuarios do banco de dados)
        return render(request, 'login.html', {'usuarios': usuario}) # renderiza os dados salvos no cadastro.html
    else:
        messages.error(request, 'As senhas não conferem')

def pegarEmail(request,email):
    usuarios = USUARIO.objects.get(email = email) # pega o usuário pelo id dele no database para modificar somente o usuário selecionado e armazena na variável usuarios
    return render(request, 'update.html', {'usuarios': usuarios}) # renderiza o id na página update.html (a mesma coisa da linha 11 )

# Função que atualiza as mudanças feitas nas informações do usuário
def update(request): 
    email = request.POST.get("email")
    n_senha = request.POST.get("senha")
    conf_senha = request.POST.get("conf_senha")
    
    if conf_senha == n_senha:
        try:
            usuarios = USUARIO.objects.get(email = email) # pega o email do usuário para modificar somente o usuário selecionado e armazena na variável usuarios
            usuarios.senha = n_senha
            usuarios.save() # salva as mudanças
            return redirect(login)
        except USUARIO.DoesNotExist:
            messages.error(request, 'Email não encontrado')
    else:
        messages.error(request, 'As senha não conferem')

def deletar(request,id):
    usuarios = USUARIO.objects.get(id = id)
    usuarios.delete()
    return redirect(cadastro)

def scan(request):
    return render(request, 'scan.html')

def login(request):
    return render(request, 'login.html')

def verificar_login(request):
    user = request.POST.get('user')
    senha = request.POST.get('senha')
    
    try:
        usuario = USUARIO.objects.get(username= user, senha= senha)
        return render(request, 'index.html')
    except:
        return render(request, 'erro.html')
    
    
# FUNÇÕES DA IA -------------------------------------------------------------------------------------------------------------------------------