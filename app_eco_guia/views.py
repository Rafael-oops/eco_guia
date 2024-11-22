from django.shortcuts import render, redirect
from .models import USUARIO, RECLAMACOE, CATEGORIA,IDEIA # importa o mapeamento do banco de dados do arquivo models.py
from django.contrib import messages
import logging
import numpy as np
import tensorflow as tf  # Este import pode ser retirado caso nao esteja em uso
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import ImageHistory  
from PIL import Image 
from tensorflow.lite.python.interpreter import Interpreter 
from django.contrib.auth.hashers import check_password
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
        messages.success(request, 'Cadastro realizado com sucesso!')
        return render(request, 'login.html', {'usuarios': usuario}) # renderiza os dados salvos no cadastro.html
    else:
        messages.error(request, 'As senhas não conferem')
        return render(request, 'cadastro.html')

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
            messages.success(request, 'Senha atualizada com sucesso!')
            return redirect(login)
        except USUARIO.DoesNotExist:
            messages.error(request, 'Email não encontrado')
            return redirect('update')
    else:
        messages.error(request, 'As senha não conferem')
        return redirect('update')

def deletar(request,id):
    usuarios = USUARIO.objects.get(id = id)
    usuarios.delete()
    return redirect(cadastro)

def scan(request):
    return render(request, 'scan.html')

def login(request):
    return render(request, 'login.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import USUARIO

def verificar_login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        senha = request.POST.get('senha')
        
        try:
            # Busca o usuário pelo username
            usuario = USUARIO.objects.get(username=user)
            
            # Verifica se a senha é igual à salva no banco
            if senha == usuario.senha:
                return render(request, 'index.html', {"conta": usuario})
            else:
                messages.error(request, 'Senha incorreta. Tente novamente.')
                return redirect('login')
        except USUARIO.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Tente novamente.')
            return redirect('login')
    else:
        return redirect('login')

    
def fale_conosco(request, id):
    usuario = USUARIO.objects.get(id=id)
    return render(request, 'reclame.html',{'user': usuario})

def salvar_reclamacao(request,id):
    id_user = USUARIO.objects.get(id=id)
    rnome = request.POST.get("nome")
    remail = request.POST.get("email")
    mensagem = request.POST.get("mensagem")
    RECLAMACOE.objects.create(id_usuario = id_user, rnome = rnome, remail = remail, mensagem= mensagem)
    return render(request, 'index.html',{'conta': id_user}) 


# IDEIAS DE RECICLAGEM -----------------------------------

def ideias(request):
    ideias = IDEIA.objects.all()
    return render(request, 'ideias.html', {'ideias': ideias})

# VASOS -----------------------------------

def vasos (request):
    return render (request, 'vasos.html')

# PORTA_RETRATO -----------------------------------

def porta_retrato (request):
    return render(request, 'porta_retrato.html')

# FUNÇÕES DA IA -------------------------------------------------------------------------------------------------------------------------------



# View para exibir o HTML na página principal
def scan(request):
    history = ImageHistory.objects.all().order_by("-last_classified")
    return render(request, "scan.html", {"history": history})

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)

# Definição das categorias de resíduos e o tamanho padrão da imagem
categories = ['casca_de_ovo', 'lixo', 'metal', 'papel', 'plastico', 'residuo_de_alimentos', 'vidro']
img_size = 224

# Caminho para o modelo TFLite
# model_path = "app_eco_guia\model\model_trained_quantized.tflite"
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'app_eco_guia', 'model', 'modelo_compativel_V2.tflite')


# Função para preparar a imagem antes da predição
def prepare_image(image, target_size):
    """
    Prepara a imagem redimensionando e normalizando os valores para o formato correto
    que o modelo espera. O tamanho alvo deve ser consistente com o treinamento do modelo.
    """
    logging.debug(f"Preparing image with target size {target_size}")
    
    # Verifica se a imagem não está no modo RGB, e converte se necessário
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Redimensiona a imagem para o tamanho esperado pelo modelo
    image = image.resize(target_size)
    
    # Converte para array numpy e normaliza os valores de pixels para [0, 1]
    image = np.array(image) / 255.0
    
    # Adiciona uma dimensão extra para representar o lote (batch), esperado pelo modelo
    image = np.expand_dims(image, axis=0)
    
    logging.debug("Image prepared successfully.")
    return image

# Função para fazer a predição da categoria do resíduo
def predict_waste(image_array, interpreter, categories):
    """
    Faz a predição da categoria do resíduo usando o modelo TensorFlow Lite.
    """
    # Obter os detalhes de entrada e saída do modelo
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    # Certificar que a imagem está no formato de array float32
    image_array = np.array(image_array, dtype=np.float32)
    
    # Coloca o tensor de entrada no interpretador
    interpreter.set_tensor(input_details["index"], image_array)
    
    # Faz a inferência (predição)
    interpreter.invoke()
    
    # Recupera os resultados das previsões
    predictions = interpreter.get_tensor(output_details["index"])

    # Obtém a classe com a maior probabilidade (resultado da predição)
    predicted_class = np.argmax(predictions, axis=1)[0]
    
    # Determina a categoria e verifica se é um resíduo válido
    category = categories[predicted_class]
    is_waste = category in categories

    return is_waste, category, predictions

# View para lidar com a predição de imagens enviadas pelo cliente
#@csrf_exempt  # Desabilita proteção CSRF, necessário para requisições POST externas
def predict(request):
    """
    Endpoint que recebe uma imagem via POST, faz a predição da categoria do resíduo
    e retorna os resultados em formato JSON.
    """
    # Verifica se o método da requisição é POST
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=400)

    # Verifica se o arquivo foi enviado no corpo da requisição
    if "file" not in request.FILES:
        return JsonResponse({"error": "Nenhum arquivo enviado"}, status=400)

    file = request.FILES["file"]

    # Verifica se o arquivo é uma imagem nos formatos suportados
    if not file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        return JsonResponse(
            {"error": "Formato de arquivo não suportado. Por favor, envie uma imagem."},
            status=400,
        )

    try:
        # Tenta abrir a imagem usando a biblioteca Pillow
        image = Image.open(file)

        # Prepara a imagem para a predição
        prepared_image = prepare_image(image, target_size=(img_size, img_size))  # Usa img_size definido globalmente

        # Carrega o modelo TFLite e aloca tensores
        interpreter = Interpreter(model_path=model_path)
        interpreter.allocate_tensors()

        # Faz a predição utilizando o modelo e a imagem preparada
        is_waste, category, predictions = predict_waste(prepared_image, interpreter, categories)
        confidence = float(np.max(predictions))  # Obtém a confiança da predição

        # Verifica se já existe uma entrada no histórico para essa categoria
        history_entry, created = ImageHistory.objects.get_or_create(
            category=category, defaults={"image": file, "count": 1}
        )

        if not created:
            # Atualiza o contador e a imagem se a categoria já existir no histórico
            history_entry.count += 1
            history_entry.image = file  # Substitui pela nova imagem enviada
            history_entry.save()

        # Obter a URL da imagem salva (caso esteja usando um armazenamento externo)
        image_url = default_storage.url(history_entry.image.name)

        # Retorna a resposta com os resultados da predição
        return JsonResponse(
            {
                "is_waste": is_waste,
                "category": category,
                "confidence": confidence,
                "image_url": image_url  # Adiciona a URL da imagem na resposta
            }
        )

    except Exception as e:
        logging.error(f"Erro ao processar a imagem: {e}")
        return JsonResponse({"error": "Erro ao processar a imagem."}, status=500)

# FUNÇÕES DO CHAT -------------------------------------------------------------------------------------------------------------------------------
# chat/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import json

# Função para carregar diálogos de um arquivo JSON
def carregar_dialogos(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        dialogos = json.load(arquivo)
    return dialogos

# Carregar o arquivo dialogos.json da pasta estática ou de outra pasta apropriada
caminho_arquivo = os.path.join(settings.BASE_DIR, 'app_eco_guia', 'static', 'dialogos.json')
dialogos = carregar_dialogos(caminho_arquivo)

# Função para responder à mensagem do usuário
def responder(entrada):
    entrada = entrada.lower()
    for categoria, respostas in dialogos.items():
        if entrada in respostas:
            return respostas[entrada]
    return "Ops!!!, Selecione uma das opções Válidas🤖."

# View que junta a rota da página inicial e o chat
def chat(request):
    if request.method == 'POST':
        # Carregar a mensagem do corpo da requisição JSON
        corpo = json.loads(request.body)  # Acessa o corpo da requisição JSON
        mensagem_usuario = corpo.get("mensagem")
        resposta = responder(mensagem_usuario)
        return JsonResponse({"resposta": resposta})
    else:
        # Se for uma requisição GET, renderiza o template do chat
        return render(request, 'index.html')

# FUNÇÕES DO MAPA -------------------------------------------------------------------------------------------------------------------------------
from .models import Marcadores

def mapa_view(request):
    tipo = request.GET.get("tipo")
    if tipo:
        pontos = Marcadores.objects.filter(tipo_material=tipo)
    else:
        pontos = Marcadores.objects.all()

    # Transformando os dados em uma lista de dicionários para ser usada no template
    pontos_data = list(pontos.values("nome", "endereco", "latitude", "longitude", "tipo_material", "horario", "descricao"))
    
    # Garantir que os dados estejam em formato JSON com aspas duplas
    pontos_json = json.dumps(pontos_data)

    # Integração das funções fale_conosco e salvar_reclamacao
    id = request.GET.get("id")  # Obtém o ID do usuário da query string, se disponível
    if id:
        usuario = get_object_or_404(USUARIO, id=id)
        if request.method == "POST":
            # Chama a função salvar_reclamacao se for uma requisição POST
            salvar_reclamacao(request, id)
        else:
            # Chama a função fale_conosco se for uma requisição GET
            fale_conosco(request, id)
    
    return render(request, "mapa.html", {"pontos": pontos_json},)
