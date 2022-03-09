# Generated by Django 3.2 on 2022-03-03 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_movies_date_premier'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_base',
            field=models.BooleanField(default=True, verbose_name='Базовая страница'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
