# Generated by Django 3.2 on 2022-01-23 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20220123_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=19, null=True, unique=True, verbose_name='Телефон'),
        ),
    ]
