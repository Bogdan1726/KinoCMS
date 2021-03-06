# Generated by Django 3.2 on 2022-03-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0025_auto_20220309_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mobile', models.BooleanField(default=False)),
                ('is_tablet', models.BooleanField(default=False)),
                ('is_touch_capable', models.BooleanField(default=False)),
                ('is_pc', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='carouselbanner',
            options={'verbose_name': 'Карусель', 'verbose_name_plural': 'Карусель'},
        ),
        migrations.AlterField(
            model_name='carouselbanner',
            name='interval',
            field=models.IntegerField(choices=[(5, '5сек'), (10, '10сек'), (30, '30сек')], default=5, verbose_name='Интервал'),
        ),
    ]
