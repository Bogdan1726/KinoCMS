# Generated by Django 3.2 on 2022-02-02 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20220130_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='seo_text_ru',
            field=models.TextField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='homepage',
            name='seo_text_ua',
            field=models.TextField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='page',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='page',
            name='description_ua',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='page',
            name='image_ru',
            field=models.ImageField(null=True, unique=True, upload_to='pages/', verbose_name='Главная картинка'),
        ),
        migrations.AddField(
            model_name='page',
            name='image_ua',
            field=models.ImageField(null=True, unique=True, upload_to='pages/', verbose_name='Главная картинка'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_ua',
            field=models.CharField(max_length=100, null=True, verbose_name='Название'),
        ),
    ]
