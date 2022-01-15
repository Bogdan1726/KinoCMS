# Generated by Django 3.2 on 2022-01-15 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(unique=True, upload_to='banners/background/', verbose_name='Баннер')),
                ('background', models.BooleanField(default=True, verbose_name='Фон')),
                ('background_image', models.BooleanField(default=False, verbose_name='Фото на фон')),
            ],
            options={
                'verbose_name': 'Баннер задний фон',
                'verbose_name_plural': 'Баннер задний фон',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерею',
            },
        ),
        migrations.CreateModel(
            name='Halls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер зала')),
                ('description', models.TextField(verbose_name='Описание зала')),
                ('layout', models.ImageField(unique=True, upload_to='halls/layout', verbose_name='Схема зала')),
                ('banner', models.ImageField(unique=True, upload_to='halls/banners', verbose_name='Верхний баннер')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
            ],
            options={
                'verbose_name': 'Залы',
                'verbose_name_plural': 'Зал',
            },
        ),
        migrations.CreateModel(
            name='HomePageBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(unique=True, upload_to='banners/home_page/', verbose_name='Баннер')),
                ('url', models.URLField(verbose_name='url')),
                ('text', models.CharField(max_length=150, verbose_name='Текст')),
                ('activate', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Баннер главной верх',
                'verbose_name_plural': 'Баннер главной верх',
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название фильма')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(unique=True, upload_to='movies/', verbose_name='Главная картинка')),
                ('link', models.URLField(verbose_name='Ссылка на трейлер')),
                ('type', models.CharField(choices=[('3d', '3D'), ('2d', '2D'), ('imax', 'IMAX')], max_length=4, verbose_name='Тип кино')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
            ],
            options={
                'verbose_name': 'Фильмы',
                'verbose_name_plural': 'Фильм',
            },
        ),
        migrations.CreateModel(
            name='PromotionsPageBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(unique=True, upload_to='banners/promotions/', verbose_name='Баннер')),
                ('url', models.URLField(verbose_name='url')),
                ('activate', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Баннер акции',
                'verbose_name_plural': 'Баненер акции',
            },
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('ticket_price', models.PositiveIntegerField(verbose_name='Цена билета')),
                ('halls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.halls', verbose_name='Зал')),
                ('movies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.movies', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'Сеансы',
                'verbose_name_plural': 'Сеанс',
            },
        ),
        migrations.CreateModel(
            name='SeoBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='url')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('keywords', models.CharField(max_length=50, verbose_name='Ключевые слова')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Seo блок',
                'verbose_name_plural': 'Seo блок',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField(verbose_name='Ряд')),
                ('place', models.PositiveIntegerField(verbose_name='Место')),
                ('type', models.BooleanField(default=True, verbose_name='Тип(покупка или бронь)')),
                ('seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.seance', verbose_name='Сеанс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Посетитель')),
            ],
            options={
                'verbose_name': 'Билеты',
                'verbose_name_plural': 'Билет',
            },
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название акции')),
                ('date_published', models.DateField(verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(unique=True, upload_to='promotions/', verbose_name='Главная картинка')),
                ('link', models.URLField(verbose_name='Ссылка на видео')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Акции',
                'verbose_name_plural': 'Акцию',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('active', models.BooleanField(default=True, verbose_name='Активна')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(unique=True, upload_to='pages/', verbose_name='Главная картинка')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Страницы',
                'verbose_name_plural': 'Страницу',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название новости')),
                ('date_published', models.DateField(verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(unique=True, upload_to='news/', verbose_name='Главная картинка')),
                ('link', models.URLField(verbose_name='Ссылка на видео')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новость',
            },
        ),
        migrations.AddField(
            model_name='movies',
            name='seo_block',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок'),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(unique=True, upload_to='gallery/', verbose_name='Картинка')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.gallery', verbose_name='Галерея')),
            ],
            options={
                'verbose_name': 'Картинки',
                'verbose_name_plural': 'Картинку',
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number1', models.CharField(max_length=15, verbose_name='')),
                ('phone_number2', models.CharField(max_length=15, verbose_name='')),
                ('active', models.BooleanField(default=True, verbose_name='')),
                ('seo_text', models.TextField(verbose_name='')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Домашняя страница',
                'verbose_name_plural': 'Домашнюю страницу',
            },
        ),
        migrations.AddField(
            model_name='halls',
            name='seo_block',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок'),
        ),
        migrations.CreateModel(
            name='ContactsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название кинотеатра')),
                ('active', models.BooleanField(default=True, verbose_name='Активна')),
                ('address', models.TextField(verbose_name='Адресс')),
                ('coordinates', models.CharField(max_length=100, verbose_name='Координаты для карты')),
                ('logo', models.ImageField(unique=True, upload_to='pages/contacts/', verbose_name='Логотип')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название кинотеатра')),
                ('description', models.TextField(verbose_name='Описание')),
                ('conditions', models.TextField(verbose_name='Условия')),
                ('logo', models.ImageField(unique=True, upload_to='cinema/logo/', verbose_name='Логотип')),
                ('photo', models.ImageField(unique=True, upload_to='cinema/photo/', verbose_name='Фото верхнего баннера')),
                ('gallery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.gallery', verbose_name='Галерея картинок')),
                ('halls', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.halls', verbose_name='Список залов')),
                ('seo_block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.seoblock', verbose_name='SEO блок')),
            ],
            options={
                'verbose_name': 'Кинотеатры',
                'verbose_name_plural': 'Кинотеатр',
            },
        ),
    ]
