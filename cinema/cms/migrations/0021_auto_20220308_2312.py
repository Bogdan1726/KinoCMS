# Generated by Django 3.2 on 2022-03-08 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_auto_20220308_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='backgroundbanner',
            name='value',
            field=models.CharField(default='banner', max_length=6),
        ),
        migrations.AlterField(
            model_name='backgroundbanner',
            name='type',
            field=models.CharField(choices=[('back', 'Просто фон'), ('img', 'Фото на фон')], default=('back', 'Просто фон'), max_length=20, verbose_name='Тип'),
        ),
    ]
