# Generated by Django 5.0 on 2024-01-26 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_PP', '0012_remove_permissao_per_jur_id_permissao_per_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Galeira_Ponto_Turistico',
            fields=[
                ('gap_id', models.AutoField(primary_key=True, serialize=False)),
                ('gap_descricao', models.CharField(max_length=512)),
                ('gap_foto', models.ImageField(blank=True, upload_to='imgsPontos/')),
                ('gap_pon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_PP.ponto_turistico')),
            ],
        ),
    ]
