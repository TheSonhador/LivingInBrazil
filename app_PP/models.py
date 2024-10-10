from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .validators import telefone

class Usuario_Fisico(models.Model):
    fis_user = models.OneToOneField(User, on_delete=models.CASCADE)
    fis_id = models.AutoField(primary_key=True)
    fis_foto = models.ImageField(upload_to='imgs/', blank = True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])
    fis_idade = models.IntegerField()
    fis_sexo = models.CharField(max_length=15)
    fis_nascimento = models.DateField()
    fis_profissao = models.CharField(max_length=100)
    fis_telefone = models.FloatField(validators=[telefone])

class Usuario_Juridico(models.Model):
    jur_user = models.OneToOneField(User, on_delete=models.CASCADE)
    jur_id = models.AutoField(primary_key=True)
    jur_nome_fantasia = models.CharField(max_length=100)
    jur_telefone = models.FloatField(validators=[telefone])
    jur_foto = models.ImageField(upload_to='imgs2/',blank = True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])

class Usuario_administrador(models.Model):
    adm_id = models.AutoField(primary_key=True)
    adm_telefone = models.FloatField(validators=[telefone])
    adm_user = models.OneToOneField(User, on_delete=models.CASCADE)

class Usuario_Governo(models.Model):
    gov_user = models.OneToOneField(User, on_delete=models.CASCADE)
    gov_id = models.AutoField(primary_key=True)
    gov_telefone = models.FloatField(validators=[telefone])
    gov_foto = models.ImageField(upload_to='imgs3/',blank = True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])


class Ponto_Turistico(models.Model):
    pon_id = models.AutoField(primary_key=True)
    pon_nome = models.CharField(max_length=100)
    pon_descricao = models.CharField(max_length=100)
    pon_qrcode = models.ImageField(upload_to='imgsPontos/',blank = True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'], 'apenas imagens são aceitas')])
    pon_latitude = models.FloatField()
    pon_longitude = models.FloatField()
    pon_status = models.BooleanField()
    pon_jur_id = models.ForeignKey(Usuario_Juridico, on_delete=models.CASCADE,blank = True, null=True)
    pon_gov_id = models.ForeignKey(Usuario_Governo, on_delete=models.CASCADE,blank = True, null=True)

class Galeira_Ponto_Turistico(models.Model):
    gap_id = models.AutoField(primary_key=True)
    gap_descricao = models.CharField(max_length=512)
    gap_foto = models.ImageField(upload_to='imgsPontos/', blank = True)
    gap_pon = models.ForeignKey(Ponto_Turistico, on_delete=models.CASCADE)

class Endereco_Turistico(models.Model):
    end_id = models.AutoField(primary_key=True)
    end_pon_id = models.OneToOneField(Ponto_Turistico, on_delete=models.CASCADE)
    end_cidade = models.CharField(max_length=100)
    end_bairro = models.CharField(max_length=100)
    end_rua = models.CharField(max_length=100)
    end_numero = models.IntegerField()

class tb_favoritos(models.Model):
    fav_id = models.AutoField(primary_key=True)
    fav_fis_id = models.ForeignKey(Usuario_Fisico, on_delete=models.CASCADE)
    fav_pon_id = models.ForeignKey(Ponto_Turistico, on_delete=models.CASCADE)

class tb_avaliacoes(models.Model):
    ava_id = models.AutoField(primary_key=True)
    ava_avaliacao = models.FloatField()
    ava_comentario = models.CharField(max_length=512)
    ava_fis_id = models.ForeignKey(Usuario_Fisico, on_delete=models.CASCADE)
    ava_nota = models.IntegerField()
    ava_pon_id = models.ForeignKey(Ponto_Turistico, on_delete=models.CASCADE)    

class tb_galeria_avaliacao(models.Model):
    gal_id = models.AutoField(primary_key=True)
    gal_descricao = models.CharField(max_length=45)
    gal_foto = models.ImageField(upload_to='imgs_pon/', blank = True)
    gal_ava_id = models.ForeignKey(tb_avaliacoes, on_delete=models.CASCADE)


class Endereco_Usuario(models.Model):
    endUser_id = models.AutoField(primary_key=True)
    endUser_user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    endUser_cidade = models.CharField(max_length=100)
    endUser_estado = models.CharField(max_length=100)
    endUser_pais = models.CharField(max_length=100)

class Permissao(models.Model):
    per_id = models.AutoField(primary_key=True)
    per_user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    per_nivelPermissao = models.CharField(max_length=100)

class PontoTuristicoAuto(models.Model):
    nome = models.CharField(max_length=100)
    resumo = models.TextField()
    url_imagem = models.URLField(blank=True, null=True)



