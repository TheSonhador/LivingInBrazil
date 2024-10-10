# Generated by Django 5.0 on 2024-01-25 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_PP', '0011_alter_ponto_turistico_pon_foto_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissao',
            name='per_jur_id',
        ),
        migrations.AddField(
            model_name='permissao',
            name='per_user_id',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
