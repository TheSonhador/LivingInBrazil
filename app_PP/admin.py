from django.contrib import admin
from .models import Usuario_Fisico, Usuario_Juridico, Ponto_Turistico, Galeira_Ponto_Turistico, Endereco_Turistico, Endereco_Usuario, Usuario_administrador, Usuario_Governo, Permissao, tb_avaliacoes, tb_galeria_avaliacao

admin.site.register(Usuario_Juridico)
admin.site.register(Usuario_Fisico)
admin.site.register(Ponto_Turistico)
admin.site.register(Galeira_Ponto_Turistico)
admin.site.register(Endereco_Turistico)
admin.site.register(Endereco_Usuario)
admin.site.register(Usuario_administrador)
admin.site.register(Usuario_Governo)
admin.site.register(Permissao)
admin.site.register(tb_avaliacoes)
admin.site.register(tb_galeria_avaliacao)

