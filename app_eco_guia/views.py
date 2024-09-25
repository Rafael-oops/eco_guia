from django.shortcuts import render, redirect
from .models import USUARIO, ImageHistory # importa o mapeamento do banco de dados do arquivo models.py
from django.contrib import messages
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import tensorflow as tf
from django.core.files.storage import default_storage

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


# View para exibir o HTML na raiz
def main(request):
    # Carregar os dados do histórico para exibir no template
    history = ImageHistory.objects.all().order_by("-last_classified")
    return render(request, "scan.html", {"history": history})


# Create your views here.




# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Definição das categorias e tamanho de imagem
categories = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
img_size = 128

# Caminho para o modelo salvo
model_path = 'app_eco_guia\model\model_trained_quantized.tflite'


# Verificar se o modelo existe
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Carregar o modelo TFLite
try:
    logging.info(f"Loading model from {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    logging.info("Model loaded successfully.")
except (OSError, ValueError) as e:
    logging.error(f"Error loading the model: {str(e)}")
    raise RuntimeError(f"Error loading the model: {str(e)}")


# Função para preparar a imagem
def prepare_image(image, target_size):
    logging.debug(f"Preparing image with target size {target_size}")
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image) / 255.0  # Normalizar a imagem
    image = np.expand_dims(image, axis=0)  # Adicionar uma dimensão de lote
    logging.debug("Image prepared successfully.")
    return image


# Função de predição
def predict_waste(image_array, interpreter, categories):
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    # Prepara a imagem
    image_array = np.array(image_array, dtype=np.float32)
    interpreter.set_tensor(input_details["index"], image_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details["index"])

    predicted_class = np.argmax(predictions, axis=1)[0]
    category = categories[predicted_class]
    is_waste = (
        category in categories
    )  # Sempre será True aqui, mas pode ajustar se necessário

    return is_waste, category, predictions


# View para predição
@csrf_exempt  # Desativa a proteção CSRF para essa view
def predict(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=400)

    # Verificar se o arquivo foi enviado corretamente
    if "file" not in request.FILES:
        return JsonResponse({"error": "Nenhum arquivo enviado"}, status=400)

    file = request.FILES["file"]

    # Verificar se o arquivo é uma imagem válida
    if not file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        return JsonResponse(
            {"error": "Formato de arquivo não suportado. Por favor, envie uma imagem."},
            status=400,
        )

    try:
        # Abrir a imagem usando o PIL
        image = Image.open(file)

        # Verifique se a função de preparação de imagem e predição está correta
        prepared_image = prepare_image(
            image, target_size=(128, 128)
        )  # O tamanho que você está esperando

        # Fazer a predição (Certifique-se que o modelo foi carregado corretamente)
        is_waste, category, predictions = predict_waste(
            prepared_image, interpreter, categories
        )
        confidence = float(np.max(predictions))

        # Salvar no histórico ou atualizar se a categoria já existe
        history_entry, created = ImageHistory.objects.get_or_create(
            category=category, defaults={"image": file, "count": 1}
        )

        if not created:
            # Atualiza o contador e a imagem se a categoria já existe
            history_entry.count += 1
            history_entry.image = file  # Substitui pela nova imagem enviada
            history_entry.save()

            # Obter a URL da imagem salva
        image_url = default_storage.url(history_entry.image.name)

        return JsonResponse(
            {
                "is_waste": is_waste,
                "category": category,
                "confidence": float(np.max(predictions)),
            }
        )

    except Exception as e:
        logging.error(f"Erro ao processar a imagem: {e}")
        return JsonResponse({"error": "Erro ao processar a imagem."}, status=500)
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor."}, status=500)
