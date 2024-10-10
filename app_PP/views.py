from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Usuario_Fisico, Usuario_Juridico, Ponto_Turistico, Endereco_Turistico, Galeira_Ponto_Turistico, tb_avaliacoes, tb_galeria_avaliacao, Endereco_Usuario, Usuario_administrador, Usuario_Governo, Permissao
from django.contrib.auth.models import User
from django.db.models import Avg, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import Form_Juridico, Form_Juridico_edit, Form_Admin, Form_Admin_edit, Form_Fisico, Form_Fisico_edit, Form_Governo, Form_Governo_edit, Form_Ponto, Form_Ponto_edit
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'PaginaInicial/index.html')


def cliente(request):
    return render(request, 'app_LIB/index.html')

def pontos_turisticos(request):

    pontos = {
        "pontos": Ponto_Turistico.objects.all(),
        'fotos': Galeira_Ponto_Turistico.objects.all()
    }

    pesquisa = request.GET.get('pesquisa')
    
    if pesquisa:
        pontos['pontos'] = pontos['pontos'].filter(
            Q(pon_nome__icontains=pesquisa)
            | Q(pon_descricao__icontains=pesquisa)
        )

    return render(request, 'app_LIB/pontos_turisticos.html', pontos)


def pt_descricao(request, id):
    ponto = Ponto_Turistico.objects.get(pon_id=id)
    endereco = Endereco_Turistico.objects.get(end_pon_id=ponto)
    galeria = Galeira_Ponto_Turistico.objects.filter(gap_pon=ponto)
    avaliacao = tb_avaliacoes.objects.filter(ava_pon_id=ponto).prefetch_related('ava_fis_id')
    galeria_avaliacao = tb_galeria_avaliacao.objects.filter(gal_ava_id__in=avaliacao)

    media_notas = avaliacao.aggregate(media=Avg('ava_nota'))['media']

    objeto = {
        'ponto': ponto,
        'endereco': endereco,
        'galeria': galeria,
        'avaliacao': avaliacao,
        'media_notas': media_notas,
        'galeria_avaliacao': galeria_avaliacao,
    }

    return render(request, 'app_LIB/pt_descricao.html', objeto)


def login_A(request):
    return render(request, 'usuarios/Admin/LoginAdm.html')

def logar_A(request):

    username = request.POST.get('nome') + request.POST.get('sobrenome')
    senha = request.POST.get('senha')

    user = authenticate(username = username, password = senha)

    if user:
        login(request, user)
        if Usuario_Governo.objects.filter(gov_user = request.user):
            userG_Logado = Usuario_Governo.objects.get(gov_user = request.user)
            request.session['user_logado'] = userG_Logado.gov_id
        elif Usuario_Juridico.objects.filter(jur_user = request.user):
            userJ_Logado = Usuario_Juridico.objects.get(jur_user = request.user)
            request.session['user_logado'] = userJ_Logado.jur_id
        elif Usuario_Fisico.objects.filter(fis_user = request.user):
            userF_Logado = Usuario_Fisico.objects.get(fis_user = request.user)
            request.session['user_logado'] = userF_Logado.fis_id      
            return redirect('cliente') 
        elif Usuario_administrador.objects.filter(adm_user = request.user):
            userA_Logado = Usuario_administrador.objects.get(adm_user = request.user)
            request.session['user_logado'] = userA_Logado.adm_id       
        return redirect('home')
    else:
        return redirect('login')

def Sair(request):
        #del request.session['user_logado']
    logout(request)
    return redirect('login')        

def registrar_F(request):
    if (request.method == 'POST'):
        form = Form_Fisico(request.POST)
        if form.is_valid():
            novo_usuario = Usuario_Fisico()
            novo_user = User()
            permissao = Permissao()

            username = request.POST.get('nome') + request.POST.get('sobrenome')
            novo_user.username = username
            novo_user.first_name = request.POST.get('nome')
            novo_user.last_name = request.POST.get('sobrenome')
            novo_user.email = request.POST.get('email')
            novo_user.set_password(request.POST.get('password'))

            novo_user.save()

            permissao.per_user_id = novo_user
            permissao.per_nivelPermissao = 'Baixo'

            permissao.save()

            novo_usuario.fis_user = novo_user
            novo_usuario.fis_nascimento = request.POST.get('nascimento')
            novo_usuario.fis_idade = request.POST.get('idade')
            novo_usuario.fis_profissao = request.POST.get('profissao')
            novo_usuario.fis_sexo = request.POST.get('sexo')
            novo_usuario.fis_telefone = request.POST.get('telefone')

            novo_usuario.fis_foto = request.FILES.get('foto')
            
            novo_usuario.save()

            return redirect('home')
        else:
            return render(request, 'usuarios/criarUsuario.html', {'form': form})
    else:
        form = Form_Fisico()
        return render(request, 'usuarios/criarUsuario.html', {'form': form})

def read(request):
    
    if request.user.is_authenticated:
        Objetos = {
            'usuarios': Usuario_Fisico.objects.all(),
            'usuariosJ': Usuario_Juridico.objects.all(),
            'users': User.objects.all()
        }
        return render(request, 'usuarios/dashboard.html', Objetos)
    else:
        return redirect('login')

def tables_f(request):
    if request.user.is_authenticated:
        Objetos = {
            'usuarios': Usuario_Fisico.objects.all(),
            'users': User.objects.all()
        }
        return render(request, 'usuarios/tables/usuario_f.html', Objetos)
    else:
        return redirect('login')

def tables_j(request):
    if request.user.is_authenticated:
        Objetos = {
            'usuariosJ': Usuario_Juridico.objects.all(),
            'users': User.objects.all()
        }

        return render(request, 'usuarios/tables/usuario_j.html', Objetos)
    else:
        return redirect('login')
    
def tables_g(request):
    if request.user.is_authenticated:
        Objetos = {
            'usuariosG': Usuario_Governo.objects.all(),
            'users': User.objects.all()
        }

        return render(request, 'usuarios/tables/usuario_g.html', Objetos)
    else:
        return redirect('login')
    
def tables_a(request):
    if request.user.is_authenticated:
        Objetos = {
            'usuariosJ': Usuario_administrador.objects.all(),
            'users': User.objects.all()
        }

        return render(request, 'usuarios/tables/usuario_a.html', Objetos)
    else:
        return redirect('login')    

def register(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            form = Form_Juridico(request.POST)
            if form.is_valid():
                novo_usuario = Usuario_Juridico()
                novo_user = User()
                permissao = Permissao()

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                novo_user.username = username
                novo_user.first_name = request.POST.get('nome')
                novo_user.last_name = request.POST.get('sobrenome')
                novo_user.email = request.POST.get('email')
                novo_user.set_password(request.POST.get('password'))

                novo_user.save()

                permissao.per_user_id = novo_user
                permissao.per_nivelPermissao = 'Medio'

                permissao.save()

                novo_usuario.jur_user = novo_user
                novo_usuario.jur_nome_fantasia = request.POST.get('nome_Fantasia')
                novo_usuario.jur_telefone = request.POST.get('telefone')

                novo_usuario.jur_foto = request.FILES.get('foto')

                novo_usuario.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Juridico/Register.html', {'form': form})
        else:
            form = Form_Juridico()
            return render(request, 'usuarios/Juridico/Register.html', {'form': form})
    else:
        return redirect('login')
    
def registrar_A(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            form = Form_Admin(request.POST)
            if form.is_valid():
                novo_usuario = Usuario_administrador()
                novo_user = User()
                permissao = Permissao()

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                novo_user.username = username
                novo_user.first_name = request.POST.get('nome')
                novo_user.last_name = request.POST.get('sobrenome')
                novo_user.email = request.POST.get('email')
                novo_user.set_password(request.POST.get('password'))
                novo_user.is_staff = True
                novo_user.is_superuser = True

                novo_user.save()

                permissao.per_user_id = novo_user
                permissao.per_nivelPermissao = 'Alto'

                permissao.save()

                novo_usuario.adm_user = novo_user
                novo_usuario.adm_telefone = request.POST.get('telefone')

                novo_usuario.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Admin/CriarAdmin.html', {'form': form})
        else:
            form = Form_Admin()
            return render(request, 'usuarios/Admin/CriarAdmin.html', {'form': form})
    else:
        return redirect('login')
    
def registrar_G(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            form = Form_Governo(request.POST)
            if form.is_valid():
                novo_usuario = Usuario_Governo()
                novo_user = User()
                permissao = Permissao()

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                novo_user.username = username
                novo_user.first_name = request.POST.get('nome')
                novo_user.last_name = request.POST.get('sobrenome')
                novo_user.email = request.POST.get('email')
                novo_user.set_password(request.POST.get('password'))

                novo_user.save()

                permissao.per_user_id = novo_user
                permissao.per_nivelPermissao = 'Medio'

                permissao.save()

                novo_usuario.gov_user = novo_user
                novo_usuario.gov_telefone = request.POST.get('telefone')

                novo_usuario.gov_foto = request.FILES.get('foto')

                novo_usuario.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Governo/CadastrarGov.html', {'form': form})
        else:
            form = Form_Governo()
            return render(request, 'usuarios/Governo/CadastrarGov.html', {'form': form})
    else:
        return redirect('login')
    
def edit(request):
    if request.user.is_authenticated:
        user = request.user
        if Usuario_administrador.objects.filter(adm_user = user):
            return redirect('editA')
        elif Usuario_Juridico.objects.filter(jur_user = user):
            return redirect('editJ')
        elif Usuario_Governo.objects.filter(gov_user = user):
            return redirect('editG')  
        elif Usuario_Fisico.objects.filter(fis_user = user):
            return redirect('editF')        
    else:
        return redirect('login')   
    
def editA(request):
    if request.user.is_authenticated:   
        id = request.session['user_logado']
        usuarioA = Usuario_administrador.objects.get(adm_id = id)
        usuario = request.user

        form = Form_Admin_edit(usuarioA = usuarioA, user = usuario)

        if (request.method == 'POST'):
            form = Form_Admin_edit(request.POST, usuarioA = usuarioA, user = usuario)
            if form.is_valid():

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                usuario.username = username
                usuario.first_name = request.POST.get('nome')
                usuario.last_name = request.POST.get('sobrenome')
                usuario.email = request.POST.get('email')
                usuario.set_password(request.POST.get('password'))

                usuario.save()

                usuarioA.adm_user = usuario
                usuarioA.adm_telefone = request.POST.get('telefone')

                usuarioA.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Admin/editAdmin.html', {'form': form})
        else:
            return render(request, 'usuarios/Admin/editAdmin.html', {'form': form})
    else:
        return redirect('login')  

def editJ(request):
    if request.user.is_authenticated:   
        id = request.session['user_logado']
        usuarioJ = Usuario_Juridico.objects.get(jur_id = id)
        usuario = request.user

        form = Form_Juridico_edit(usuarioJ = usuarioJ, user = usuario)

        if (request.method == 'POST'):
            form = Form_Juridico_edit(request.POST, usuarioJ = usuarioJ, user = usuario)
            if form.is_valid():

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                usuario.username = username
                usuario.first_name = request.POST.get('nome')
                usuario.last_name = request.POST.get('sobrenome')
                usuario.email = request.POST.get('email')
                usuario.set_password(request.POST.get('password'))

                usuario.save()

                usuarioJ.jur_user = usuario
                usuarioJ.jur_telefone = request.POST.get('telefone')
                usuarioJ.jur_nome_fantasia = request.POST.get('nome_Fantasia')
                usuarioJ.jur_foto = request.FILES.get('foto')

                usuarioJ.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Juridico/editJuridico.html', {'form': form})
        else:
            return render(request, 'usuarios/Juridico/editJuridico.html', {'form': form})
    else:
        return redirect('login')

def editG(request):
    if request.user.is_authenticated:   
        id = request.session['user_logado']
        usuarioG = Usuario_Governo.objects.get(gov_id = id)
        usuario = request.user

        form = Form_Governo_edit(usuarioG = usuarioG, user = usuario)

        if (request.method == 'POST'):
            form = Form_Governo_edit(request.POST, usuarioG = usuarioG, user = usuario)
            if form.is_valid():

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                usuario.username = username
                usuario.first_name = request.POST.get('nome')
                usuario.last_name = request.POST.get('sobrenome')
                usuario.email = request.POST.get('email')
                usuario.set_password(request.POST.get('password'))

                usuario.save()

                usuarioG.gov_user = usuario
                usuarioG.gov_telefone = request.POST.get('telefone')
                usuarioG.gov_foto = request.FILES.get('foto')

                usuarioG.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/Governo/editGoverno.html', {'form': form})
        else:
            return render(request, 'usuarios/Governo/editGoverno.html', {'form': form})
    else:
        return redirect('login')   

def editF(request):
    if request.user.is_authenticated:   
        id = request.session['user_logado']
        usuarioF = Usuario_Fisico.objects.get(fis_id = id)
        usuario = request.user

        form = Form_Fisico_edit(usuarioF = usuarioF, user = usuario)

        if (request.method == 'POST'):
            form = Form_Fisico_edit(request.POST, usuarioF = usuarioF, user = usuario)
            if form.is_valid():

                username = request.POST.get('nome') + request.POST.get('sobrenome')
                usuario.username = username
                usuario.first_name = request.POST.get('nome')
                usuario.last_name = request.POST.get('sobrenome')
                usuario.email = request.POST.get('email')
                usuario.set_password(request.POST.get('password'))

                usuario.save()

                usuarioF.fis_user = usuario
                usuarioF.fis_nascimento = request.POST.get('nascimento')
                usuarioF.fis_idade = request.POST.get('idade')
                usuarioF.fis_profissao = request.POST.get('profissao')
                usuarioF.fis_sexo = request.POST.get('sexo')
                usuarioF.fis_telefone = request.POST.get('telefone')

                usuarioF.fis_foto = request.FILES.get('foto')
                
                usuarioF.save()

                return redirect('home')
            else:
                return render(request, 'usuarios/editFisico.html', {'form': form})
        else:
            return render(request, 'usuarios/editFisico.html', {'form': form})
    else:
        return redirect('login')      
    
def excluirFisico(request, id):
    UsuarioAExcluir = Usuario_Fisico.objects.get(fis_id=id)
    Users = User.objects.all()

    for user in Users:
        if (Usuario_Fisico.objects.filter(fis_user = user)):
            UserAExcluir = user
        else:
            pass

    UsuarioAExcluir.delete()
    UserAExcluir.delete()

    return redirect('home')

def excluirJuridico(request, id):
    UsuarioAExcluir = Usuario_Juridico.objects.get(jur_id=id)
    Users = User.objects.all()

    for user in Users:
        if (Usuario_Juridico.objects.filter(jur_user = user)):
            UserAExcluir = user
        else:
            pass

    UsuarioAExcluir.delete()
    UserAExcluir.delete()

    return redirect('home')

def excluirAdmin(request, id):
    UsuarioAExcluir = Usuario_administrador.objects.get(adm_id=id)
    Users = User.objects.all()

    for user in Users:
        if (Usuario_administrador.objects.filter(adm_user = user)):
            UserAExcluir = user

        else:
            pass

    UsuarioAExcluir.delete()
    UserAExcluir.delete()

    return redirect('home')

def excluirGoverno(request, id):
    UsuarioAExcluir = Usuario_Governo.objects.get(gov_id=id)
    Users = User.objects.all()

    for user in Users:
        if (Usuario_Governo.objects.filter(gov_user = user)):
            UserAExcluir = user
        else:
            pass

    UsuarioAExcluir.delete()
    UserAExcluir.delete()

    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        if Usuario_Governo.objects.filter(gov_user = request.user):
            user_logado = Usuario_Governo.objects.get(gov_id = request.session['user_logado'])

        elif Usuario_Juridico.objects.filter(jur_user = request.user):
            user_logado = Usuario_Juridico.objects.get(jur_id = request.session['user_logado'])

        elif Usuario_administrador.objects.filter(adm_user = request.user):
            user_logado = Usuario_administrador.objects.get(adm_id = request.session['user_logado'])

        elif Usuario_Fisico.objects.filter(fis_user = request.user):
            user_logado = Usuario_Fisico.objects.get(fis_id = request.session['user_logado'])
            
        Objetos = {
            'usuarios': Usuario_Fisico.objects.all(),
            'usuariosJ': Usuario_Juridico.objects.all(),
            'usuariosG': Usuario_Governo.objects.all(),
            'usuariosA': Usuario_administrador.objects.all(),
            'users': User.objects.all(),
            'pontos': Ponto_Turistico.objects.all(),
            'enderecos': Endereco_Turistico.objects.all(),
            'fotos': Galeira_Ponto_Turistico.objects.all(),
            'permissoes': Permissao.objects.all(),
            'user_logado': user_logado
        }
        return render(request, 'home.html', Objetos)
    else:
        return redirect('login')


def cadastrarPonto(request):
    if request.user.is_authenticated:
        objetos = {
            'UsuariosG': Usuario_Governo.objects.all(),
            'UsuariosJ': Usuario_Juridico.objects.all(),
            'users': User.objects.all(),
            'form': Form_Ponto()
        }
        if (request.method == 'POST'):
            objetos2 = {
                'UsuariosG': Usuario_Governo.objects.all(),
                'UsuariosJ': Usuario_Juridico.objects.all(),
                'users': User.objects.all(),                
                'form': Form_Ponto(request.POST)
            }            
            if Form_Ponto(request.POST).is_valid():
                novo_Ponto = Ponto_Turistico()
                novo_Endereco = Endereco_Turistico()
                nova_foto = Galeira_Ponto_Turistico()

                novo_Ponto.pon_nome = request.POST.get('nome')
                novo_Ponto.pon_descricao = request.POST.get('descricao')
                novo_Ponto.pon_latitude = request.POST.get('latitude')
                novo_Ponto.pon_longitude = request.POST.get('longitude')
                novo_Ponto.pon_qrcode = request.FILES.get('QRcode')
                novo_Ponto.pon_status = 0
                #usuario = request.POST.get('dono')
                if (User.objects.filter(username=request.POST.get('dono'))):
                    usuario = User.objects.get(username=request.POST.get('dono'))
                    if (Usuario_Juridico.objects.filter(jur_user = usuario)):
                        user = Usuario_Juridico.objects.get(jur_user = usuario)
                        novo_Ponto.pon_jur_id = user
                    elif (Usuario_Governo.objects.filter(gov_user = usuario)):
                        user2 = Usuario_Governo.objects.get(gov_user = usuario)
                        novo_Ponto.pon_gov_id = user2

                novo_Ponto.save()

                novo_Endereco.end_pon_id = novo_Ponto
                novo_Endereco.end_cidade = request.POST.get('cidade')
                novo_Endereco.end_bairro = request.POST.get('bairro')
                novo_Endereco.end_rua = request.POST.get('rua')
                novo_Endereco.end_numero = request.POST.get('numero')
                
                novo_Endereco.save()

                if request.FILES.get('foto') != None:
                    nova_foto.gap_foto = request.FILES.get('foto')
                    nova_foto.gap_pon = novo_Ponto
                    nova_foto.save()

                return redirect('home')
            else:
                return render(request, 'pontos/create.html', objetos2)         
        return render(request, 'pontos/create.html', objetos)
    else:
        return redirect('login')

def status_Ponto(request, id):
    if request.user.is_authenticated:
        ponto = Ponto_Turistico.objects.get(pon_id=id)

        if ponto.pon_status == 0:
            ponto.pon_status = 1
        elif ponto.pon_status == 1:
            ponto.pon_status = 0 

        ponto.save()

        return redirect('home')
    else:
        return redirect('login')       


def editarPonto(request, id):
    if request.user.is_authenticated:
        if Usuario_Governo.objects.filter(gov_user = request.user):
            user_logado = Usuario_Governo.objects.get(gov_id = request.session['user_logado'])

        elif Usuario_Juridico.objects.filter(jur_user = request.user):
            user_logado = Usuario_Juridico.objects.get(jur_id = request.session['user_logado'])

        elif Usuario_administrador.objects.filter(adm_user = request.user):
            user_logado = Usuario_administrador.objects.get(adm_id = request.session['user_logado'])

        ponto = Ponto_Turistico.objects.get(pon_id=id)
        endereco = Endereco_Turistico.objects.get(end_pon_id=id)
        Objeto = {
            'UsuariosG': Usuario_Governo.objects.all(),
            'UsuariosJ': Usuario_Juridico.objects.all(),
            'user_logado': user_logado,
            'UsuariosA': Usuario_administrador.objects.all(),
            'users': User.objects.all(),
            'ponto': Ponto_Turistico.objects.get(pon_id=id),
            'enderecos': Endereco_Turistico.objects.get(end_pon_id=id),
            'form': Form_Ponto_edit(ponto = ponto, endereco = endereco),
        }
        return render(request, 'pontos/edit.html', Objeto)
    else:
        return redirect('login')


def editPonto(request, id):
    if request.user.is_authenticated:
        ponto = Ponto_Turistico.objects.get(pon_id=id)
        endereco = Endereco_Turistico.objects.get(end_pon_id=id) 
        user = request.user
        nova_foto = Galeira_Ponto_Turistico()


        ponto.pon_nome = request.POST.get('nome')
        ponto.pon_descricao = request.POST.get('descricao')
        ponto.pon_latitude = request.POST.get('latitude')
        ponto.pon_longitude = request.POST.get('longitude')
        ponto.pon_qrcode = request.FILES.get('QRcode')

        if Usuario_administrador.objects.filter(adm_user = user):
            usuario = User.objects.get(username=request.POST.get('dono'))
            
            if (Usuario_Juridico.objects.filter(jur_user = usuario)):
                user2 = Usuario_Juridico.objects.get(jur_user = usuario)
                ponto.pon_jur_id = user2
            elif (Usuario_Governo.objects.filter(gov_user = usuario)):
                user3 = Usuario_Governo.objects.get(gov_user = usuario)
                ponto.pon_gov_id = user3

        ponto.save()

        if request.FILES.get('Nova_foto') != None:
            nova_foto.gap_foto = request.FILES.get('Nova_foto')
            nova_foto.gap_pon = ponto
            nova_foto.save()

        endereco.end_cidade = request.POST.get('cidade')
        endereco.end_bairro = request.POST.get('bairro')
        endereco.end_rua = request.POST.get('rua')
        endereco.end_numero = request.POST.get('numero')

        endereco.save()

        return redirect('home')
    else:
        return redirect('login')    
    

def excluirFoto(request, id):
    FotoAExcluir = Galeira_Ponto_Turistico.objects.get(gap_id=id)
    FotoAExcluir.delete()

    return redirect('home')

def excluirPonto(request, id):
    PontoAExcluir = Ponto_Turistico.objects.get(pon_id=id)
    PontoAExcluir.delete()

    return redirect('home')
