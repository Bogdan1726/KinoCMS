import re

from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import *


class CmsHomePageUpdateForm(forms.ModelForm):
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


class CmsPageUpdateForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ['seo_block', 'gallery']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('blah').src = window.URL.createObjectURL(this.files[0])"})

        }


class CmsImageForm(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ('gallery', )

        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'})

        }


CmsImageFormSet = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)


class CmsSeoBlockForm(forms.ModelForm):
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
