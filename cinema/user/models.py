from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib import auth
from django.db import models


# Create your models here.


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    LANGUAGE = [
        ('ru', 'Русский'),
        ('ua', 'Украинский')
    ]

    GENDER = [
        ('m', 'Мужской'),
        ('f', 'Женский')
    ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150, unique=True, validators=[username_validator],
                                verbose_name='Псевдоним')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата присоединения')
    address = models.CharField(max_length=100, blank=True, verbose_name='Адресс')
    language = models.CharField(max_length=2, default=LANGUAGE[0][0], choices=LANGUAGE, verbose_name='Язык')
    gender = models.CharField(max_length=5, default='', choices=GENDER, verbose_name='Пол')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    number_card = models.CharField(max_length=19, blank=True, verbose_name='Номер карты')
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Town(models.Model):
    town_name = models.CharField(max_length=30, verbose_name='Город')

    class Meta:
        verbose_name = 'Город пользователя'
        verbose_name_plural = 'Город пользователя'

    def __str__(self):
        return f'{self.town_name}'


