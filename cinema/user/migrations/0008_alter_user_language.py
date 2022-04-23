# Generated by Django 3.2 on 2022-04-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('ru', 'Russian'), ('uk', 'Ukrainian')], default='ru', max_length=15),
        ),
    ]
