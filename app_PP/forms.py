from django import forms
from .validators import telefone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from .models import Usuario_Juridico, Usuario_Governo, Ponto_Turistico, Endereco_Turistico
from itertools import chain

class Form_Juridico(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    nome_Fantasia = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])

class Form_Governo(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])


class Form_Admin(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])

class Form_Admin_edit(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField(required=True)
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])

    def __init__(self, *args, **kwargs):
        usuarioA = kwargs.pop('usuarioA')
        user = kwargs.pop('user')
        super(Form_Admin_edit, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = user.first_name
        self.fields['sobrenome'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['telefone'].initial = usuarioA.adm_telefone

class Form_Juridico_edit(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    nome_Fantasia = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])


    def __init__(self, *args, **kwargs):
        usuarioJ = kwargs.pop('usuarioJ')
        user = kwargs.pop('user')
        super(Form_Juridico_edit, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = user.first_name
        self.fields['sobrenome'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['telefone'].initial = usuarioJ.jur_telefone
        self.fields['nome_Fantasia'].initial = usuarioJ.jur_nome_fantasia
        if usuarioJ.jur_foto != None:
            self.fields['foto'].initial = usuarioJ.jur_foto

class Form_Governo_edit(forms.Form):
    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])


    def __init__(self, *args, **kwargs):
        usuarioG = kwargs.pop('usuarioG')
        user = kwargs.pop('user')
        super(Form_Governo_edit, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = user.first_name
        self.fields['sobrenome'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['telefone'].initial = usuarioG.gov_telefone
        if usuarioG.gov_foto != None:
            self.fields['foto'].initial = usuarioG.gov_foto


class Form_Fisico(forms.Form):

    Sexo = (
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino')
    )

    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    nascimento = forms.DateField()
    idade = forms.FloatField()
    profissao = forms.CharField()
    sexo = forms.ChoiceField(choices=Sexo)
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])


class Form_Fisico_edit(forms.Form):

    Sexo = (
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino')
    )

    nome = forms.CharField()
    sobrenome = forms.CharField()
    email = forms.EmailField()
    password = forms.FloatField()
    #senha = forms.PasswordInput()
    telefone = forms.FloatField(validators=[telefone])
    nascimento = forms.DateField()
    idade = forms.FloatField()
    profissao = forms.CharField()
    sexo = forms.ChoiceField(choices=Sexo)
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])

    def __init__(self, *args, **kwargs):
        usuarioF = kwargs.pop('usuarioF')
        user = kwargs.pop('user')
        super(Form_Fisico_edit, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = user.first_name
        self.fields['sobrenome'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['telefone'].initial = usuarioF.fis_telefone
        if usuarioF.fis_foto != None:
            self.fields['foto'].initial = usuarioF.fis_foto
        self.fields['nascimento'].initial = usuarioF.fis_nascimento
        self.fields['idade'].initial = usuarioF.fis_idade
        self.fields['profissao'].initial = usuarioF.fis_profissao
        self.fields['sexo'].initial = usuarioF.fis_sexo

class Form_Ponto(forms.Form,):
    nome = forms.CharField()
    descricao = forms.CharField()
    cidade = forms.CharField()
    bairro = forms.CharField()
    rua = forms.CharField()
    numero = forms.FloatField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])
    QRcode = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])

    #users = User.objects.all()
    #Usuarios1 = []
    #Juridico = Usuario_Juridico.objects.all()
    #Governo = Usuario_Governo.objects.all()

    #Usuarios3 = Juridico.union(Governo)
    #dono = forms.ChoiceField()
    #for usuario in users:
    #    if (Usuario_Juridico.objects.filter(jur_user = usuario)):
    #        Usuarios1.append([usuario.username,usuario.username])
    #    elif (Usuario_Governo.objects.filter(gov_user = usuario)):
    #        Usuarios1.append([usuario.username,usuario.username])
    #dono = forms.ModelChoiceField(queryset = User.objects.all())


class Form_Ponto_edit(forms.Form):
    nome = forms.CharField()
    descricao = forms.CharField()
    cidade = forms.CharField()
    bairro = forms.CharField()
    rua = forms.CharField()
    numero = forms.FloatField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    Nova_foto = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])
    QRcode = forms.ImageField(required=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])    
    def __init__(self, *args, **kwargs):
        ponto = kwargs.pop('ponto')
        endereco = kwargs.pop('endereco')
        super(Form_Ponto_edit, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = ponto.pon_nome
        self.fields['descricao'].initial = ponto.pon_descricao
        self.fields['cidade'].initial = endereco.end_cidade
        self.fields['bairro'].initial = endereco.end_bairro
        self.fields['rua'].initial = endereco.end_rua
        self.fields['numero'].initial = endereco.end_numero
        self.fields['latitude'].initial = ponto.pon_latitude
        self.fields['longitude'].initial = ponto.pon_longitude
        self.fields['QRcode'].initial = ponto.pon_qrcode
