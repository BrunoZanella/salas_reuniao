# Generated by Django 5.0.1 on 2024-12-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_delete_configuracaosistema'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite_reservas_por_usuario', models.PositiveIntegerField(default=5)),
            ],
            options={
                'verbose_name': 'Configuração do Sistema',
                'verbose_name_plural': 'Configurações do Sistema',
            },
        ),
    ]
