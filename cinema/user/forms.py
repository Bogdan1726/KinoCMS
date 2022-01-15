from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django import forms
import datetime


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(attrs={'autofocus': True}))

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateForm(UserChangeForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'error_date': 'Дата рождения не может быть позже текущей даты',
        'error_phone': 'Неверный формат номера телефона попробуйте 0(код оператора) 000 00 00',
        'error_number_card': 'Номер карты неверного формата'
    }

    new_password1 = forms.CharField(
        label=_("New password"),
        required=False,
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        required=False,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'address', 'language', 'gender', 'phone_number',
                  'date_of_birth', 'number_card', 'town',
                  'new_password1', 'new_password2'
                  ]

        widgets = {
            'language': forms.RadioSelect(),
            'gender': forms.RadioSelect(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Пример (0931231221)'}),
            'number_card': forms.TextInput(attrs={'placeholder': '16-ти значный номер вашей карты'})
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth is not None:
            if date_of_birth > datetime.date.today():
                raise forms.ValidationError(
                    self.error_messages['error_date']
                )
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) > 0:
            if phone_number.isdigit():
                if len(phone_number) < 10:
                    raise forms.ValidationError(
                        self.error_messages['error_phone']
                    )
            if not phone_number.isdigit():
                raise forms.ValidationError(
                    self.error_messages['error_phone']
                )
        return phone_number

    def clean_number_card(self):
        number_card = self.cleaned_data['number_card']
        if len(number_card) > 0:
            if number_card.isdigit():
                if len(number_card) < 16:
                    raise forms.ValidationError(
                        self.error_messages['error_number_card']
                    )
            if not number_card.isdigit():
                raise ValidationError(
                    self.error_messages['error_number_card']
                )
        return number_card

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 == '' and password2 == '':
            return password2
        if password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('new_password1') != '':
            user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user
