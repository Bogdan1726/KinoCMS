import re
from django import forms
from django.forms import modelformset_factory
from PIL import Image
from django.core.files.images import get_image_dimensions

from .models import *


class CmsHomePageUpdateForm(forms.ModelForm):
    """
    Form Home Page
    """
    error_messages = {
        'error_phone_number': 'Неверный формат номера телефона',
    }

    class Meta:
        model = HomePage
        fields = ['phone_number1', 'phone_number2', 'active', 'seo_text']

        widgets = {
            'phone_number1': forms.TextInput(attrs={'class': 'form-control',
                                                    'data-mask': '000-00-00'}),
            'phone_number2': forms.TextInput(attrs={'class': 'form-control',
                                                    'data-mask': '000-00-00'}),
            'seo_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }

    def clean_phone_number1(self):
        phone_number1 = self.cleaned_data['phone_number1']
        if len(phone_number1) < 9:
            raise forms.ValidationError(
                self.error_messages['error_phone_number']
            )
        return phone_number1

    def clean_phone_number2(self):
        phone_number2 = self.cleaned_data['phone_number2']
        if len(phone_number2) < 9:
            raise forms.ValidationError(
                self.error_messages['error_phone_number']
            )
        return phone_number2


class CmsPageUpdateForm(forms.ModelForm):
    """
    Form Pages
    """

    class Meta:
        model = Page
        exclude = ['seo_block', 'gallery']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"})

        }


class CmsContactsPageUpdateForm(forms.ModelForm):
    """
    Form Contacts Page
    """

    class Meta:
        model = ContactsPage
        exclude = ('creation_date', 'seo_block')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название кинотеатра'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'placeholder': 'Адресс кинотеатра'}),
            'coordinates': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Координаты для карты'}),
            'logo': forms.FileInput(attrs={'type': 'file',
                                           'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"})

        }


CmsContactsPageFormSet = modelformset_factory(ContactsPage, form=CmsContactsPageUpdateForm, extra=0)


class CmsPromotionCreateForm(forms.ModelForm):
    """
    Form Promotions
    """

    class Meta:
        model = Promotions
        exclude = ('gallery', 'seo_block')

        widgets = {
            'is_published': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название акции'}),
            'date_published': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"}),

            'link': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Ссылка на видео в youtube'}),
        }


class CmsImageForm(forms.ModelForm):
    """
    Form Image
    """
    error_messages = {
        'error_image': 'Размер изображения должен быть 1000x190'
    }

    class Meta:
        model = Images
        exclude = ('gallery',)

        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'})
        }

    def clean_image(self):
        images = self.cleaned_data['image']
        if self.cleaned_data:
            width, height = get_image_dimensions(images)
            if width != 1000 or height != 190:
                raise forms.ValidationError(
                    self.error_messages['error_image']
                )
        return images


CmsImageFormSet = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)


class CmsSeoBlockForm(forms.ModelForm):
    """
    Form Seo Block
    """
    error_messages = {
        'keywords': 'error_messages'
    }

    class Meta:
        model = SeoBlock
        fields = '__all__'

        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control',
                                         'placeholder': 'url'}),
            'title_seo': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'title'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'keywords'}),
            'description_seo': forms.Textarea(attrs={'class': 'form-control',
                                                     'rows': 3,
                                                     'placeholder': 'description'})
        }
