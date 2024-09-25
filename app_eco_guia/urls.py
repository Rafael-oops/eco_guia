from django.urls import path
from . import views
from app_eco_guia.views import main, predict
from django.conf import settings
from django.conf.urls.static import static
#  Crie as rotas da views aqui

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('salvar/', views.salvar, name='salvar'),
    path('editar/<str:email>', views.pegarEmail, name='editar'),
    path('update/', views.update, name='update'), # cria a rota update com o id do usuário chamando a função update do arquivo views.py (ver linha 31 do arquivo views.py) e nomeia de 'update' para o update.html encontrá-lo (ver linha 16 de update.html)
    path('delete/<int:id>', views.deletar, name='delete'),
    path('scan/', views.scan, name='scan'),
    path('verificar_login', views.verificar_login, name='verificar_login'),
    path('main/', main, name='main'),  
    path('predict/', predict, name='predict')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)