from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormView

from user.forms import UserUpdateForm
from user.models import User
from .forms import *
from .models import *


# Create your views here.


# users
class CmsUserListView(ListView):
    """
    List Users
    """
    model = User
    context_object_name = 'users'
    template_name = 'cms/pages/users/list_users.html'


class CmsUserUpdateView(UpdateView):
    """
    Update User if request.user.is_superuser
    """
    model = User
    template_name = 'cms/pages/users/update_user.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm

    def form_valid(self, form):
        if self.request.user.is_superuser:
            self.object = form.save()
            username = form.cleaned_data['username']
            messages.success(self.request, f'Данные пользователя {username} обновлены')
            return super().form_valid(form)
        messages.warning(self.request, 'Для редактирования пользователей нужно иметь права администратора')
        return redirect('users')

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsUserDeleteView(DeleteView):
    """
    Delete users if request.user.is_superuser
    """
    model = User
    success_url = reverse_lazy('users')
    template_name = 'cms/pages/users/list_users.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.success(request, 'Пользователь удалён!')
            return self.delete(request, *args, **kwargs)
        messages.warning(request, 'Для удаления пользователей нужно иметь права администратора')
        return redirect('users')


# users end


# pages
class CmsPagesListView(ListView):
    """
    list of pages
    """
    model = Page
    context_object_name = 'pages'
    template_name = 'cms/pages/page/list_pages.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPagesListView, self).get_context_data()
        context['home_pages'] = HomePage.objects.all()
        context['contacts_pages'] = ContactsPage.objects.all()
        return context


class CmsHomePageUpdateView(UpdateView):
    """
    Update a CMS home page
    """
    model = HomePage
    template_name = 'cms/pages/page/main_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsHomePageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHomePageUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if seo_block_form.is_valid():
            seo_block_form.save()
            home_page = form.save(commit=False)
            home_page.seo_block = seo_block_form.instance
            home_page.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsPageUpdateView(UpdateView):
    """
    Update a CMS pages
    """
    model = Page
    template_name = 'cms/pages/page/other_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsPageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPageUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None, instance=self.object.seo_block)
        context['formset_gallery'] = CmsImageFormSet(self.request.POST or None,
                                                     self.request.FILES or None,
                                                     queryset=Images.objects.filter(gallery=self.object.gallery))

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        formset_gallery = context['formset_gallery']
        if seo_block_form.is_valid() and formset_gallery.is_valid():
            seo_block_form.save()
            for image in formset_gallery:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = self.object.gallery
                        images.save()
            formset_gallery.save()
            page = form.save(commit=False)
            page.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsContactsUpdateView(UpdateView):
    """
        Update a CMS contacts page
    """
    model = ContactsPage
    template_name = 'cms/pages/page/contacts_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsContactsPageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsContactsUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['contacts_formset'] = CmsContactsPageFormSet(self.request.POST or None,
                                                             self.request.FILES or None,
                                                             queryset=ContactsPage.objects.filter(id=self.object.id))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if seo_block_form.is_valid():
            print('soe ok')
            seo_block_form.save()
            formset = form.save(commit=False)
            formset.seo_block = seo_block_form.instance
            formset.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            print('ok')
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        print('invalid')
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# pages end

# promotions

class CmsPromotionListView(ListView):
    """
    list of promotion
    """
    model = Promotions
    context_object_name = 'promotions'
    template_name = 'cms/pages/promotions/list_promotions.html'


class CmsPromotionCreateView(CreateView):
    """
    Create a new promotion
    """
    model = Promotions
    template_name = 'cms/pages/promotions/create_promotions.html'
    form_class = CmsPromotionCreateForm
    success_url = reverse_lazy('promotions')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPromotionCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['formset_gallery'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        formset_gallery = context['formset_gallery']
        if seo_block_form.is_valid() and formset_gallery.is_valid():
            seo_block_form.save()
            promotion = form.save(commit=False)
            promotion.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=promotion.title)
            promotion.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in formset_gallery:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = promotion.gallery
                        images.save()
            formset_gallery.save()
            promotion.save()

            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        print('invalid')
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsPromotionsUpdateView(UpdateView):
    """
    Update a promotions
    """
    model = Promotions
    template_name = 'cms/pages/promotions/update_promotions.html'
    form_class = CmsPromotionCreateForm
    success_url = reverse_lazy('promotions')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPromotionsUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['formset_gallery'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        formset_gallery = context['formset_gallery']
        if seo_block_form.is_valid() and formset_gallery.is_valid():
            seo_block_form.save()
            promotion = form.save(commit=False)
            promotion.seo_block = seo_block_form.instance
            for image in formset_gallery:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = self.object.gallery
                        images.save()
            formset_gallery.save()
            promotion.save()

            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        print('invalid')
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsPromotionDeleteView(DeleteView):
    model = Promotions
    template_name = 'cms/pages/promotions/list_promotions.html'
    success_url = reverse_lazy('promotions')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Акция удалена!')
        return self.delete(request, *args, **kwargs)





# promotions end

def index(request):
    return render(request, 'cms/elements/base.html')


def list_movie(request):
    return render(request, 'cms/pages/movies/list_movie.html')


def page_movie(request):
    return render(request, 'cms/pages/movies/page_movie.html')


def statistics(request):
    return render(request, 'cms/pages/statistics.html')


def banners(request):
    return render(request, 'cms/pages/banners.html')


def cinemas(request):
    return render(request, 'cms/pages/cinemas/list_cinemas.html')


def news(request):

    return render(request, 'cms/pages/news/list_news.html')


def promotions(request):
    return render(request, 'cms/pages/promotions/list_promotions.html')


def mailing(request):
    return render(request, 'cms/pages/mailing/mailing.html')
