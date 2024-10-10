from django.contrib import admin
from django.urls import path
from .views import index, home, cliente, read, register, registrar_F, registrar_A, registrar_G, logar_A, login_A, Sair, edit, editA, editJ, editG, editF, excluirFisico, excluirJuridico, excluirAdmin, excluirGoverno, cadastrarPonto, status_Ponto, editarPonto, excluirPonto, tables_j, tables_f, tables_g, tables_a, editPonto, excluirFoto, pontos_turisticos, pt_descricao
#registrar_J
#salvar_A,
#salvar,
#salvarPonto,

urlpatterns = [
    path('', index, name='PaginaInicial/'),

    path('cliente/', cliente, name='cliente'),
    path('pontos_turisticos/', pontos_turisticos, name='pontos_turisticos'),
    path('pontos_turisticos/<int:id>/', pt_descricao, name='pt_descricao'),

    path('registrar_F/', registrar_F, name='register_F'),
    #path('salvar/', salvar, name='salvar'),

    path('registrar_Admin/', registrar_A, name='registrar_Admin'),
    #path('salvar_Admin/', salvar_A, name='salvar_Admin'),
    path('login/', login_A, name='login'),
    path('logar/', logar_A, name='logar_Admin'),
    path('logout/', Sair, name='logout'),

    path('read/', read, name='read'),
    path('tables/usuario_f', tables_f, name='tables/usuario_f'),
    path('tables/usuario_j', tables_j, name='tables/usuario_j'),
    path('tables/usuario_g', tables_g, name='tables/usuario_g'),
    path('tables/usuario_a', tables_a, name='tables/usuario_a'),

    path('edit/', edit, name='edit'),
    path('edit_A/', editA, name='editA'),
    path('edit_J/', editJ, name='editJ'),
    path('edit_G/', editG, name='editG'),
    path('edit_F/', editF, name='editF'),            

    path('excluirFisico/<int:id>/', excluirFisico, name='excluir_F'),
    path('excluirJuridico/<int:id>/', excluirJuridico, name='excluir_J'),
    path('excluirAdmin/<int:id>/', excluirAdmin, name='excluir_A'),
    path('excluirGoverno/<int:id>/', excluirGoverno, name='excluir_G'),


    path('register/', register, name='register'),
    #path('registrar_J', registrar_J, name='registrar_J'),

    path('registrar_Gov/', registrar_G, name='registrar_G'),

    path('home/', home, name='home'),
    path('CadastrarPontos/', cadastrarPonto, name='registrar_P'),
    #path('salvarPonto/', salvarPonto, name='salvarPonto'),
    path('TrocarStatus_P/<int:id>/', status_Ponto, name='status_P'),
    path('editarPonto/<int:id>/', editarPonto, name='editar_P'),
    path('editPonto/<int:id>/', editPonto, name='editP'),
    path('excluir_Foto/<int:id>/', excluirFoto, name='excluir_Foto'),
    path('excluirPonto/<int:id>/', excluirPonto, name='excluir_P'),

    
]