# Generated by Django 5.1.5 on 2025-02-17 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Site')),
                ('url', models.URLField(verbose_name='URL do Site')),
                ('icone', models.ImageField(blank=True, null=True, upload_to='icones/', verbose_name='Ícone (PNG)')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição do Site')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
    ]
