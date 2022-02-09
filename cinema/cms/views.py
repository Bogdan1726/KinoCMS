from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
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
    Create a CMS home page
    """
    model = HomePage
    template_name = 'cms/pages/page/main_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsHomePageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHomePageUpdateView, self).get_context_data()
        if self.request.method == 'POST':
            context['seo_block_form'] = CmsSeoBlockForm(self.request.POST, instance=self.object.seo_block)
        else:
            context['seo_block_form'] = CmsSeoBlockForm(instance=self.object.seo_block)
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

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsPageUpdateView(UpdateView):
    """
    Create a CMS pages
    """
    model = Page
    template_name = 'cms/pages/page/other_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsPageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPageUpdateView, self).get_context_data()
        if self.request.method == 'POST':
            context['seo_block_form'] = CmsSeoBlockForm(self.request.POST, instance=self.object.seo_block)
            context['formset_gallery'] = CmsImageFormSet(self.request.POST, self.request.FILES,
                                                         queryset=Images.objects.filter(gallery=self.object.gallery))
        else:
            context['seo_block_form'] = CmsSeoBlockForm(instance=self.object.seo_block)
            context['formset_gallery'] = CmsImageFormSet(queryset=Images.objects.filter(gallery=self.object.gallery))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        formset_gallery = context['formset_gallery']
        if seo_block_form.is_valid():
            seo_block_form.save()
        if formset_gallery.is_valid():
            for image in formset_gallery:
                if image.cleaned_data:
                    images = image.save(commit=False)
                    images.gallery = self.object.gallery
                    images.save()
            formset_gallery.save()
        page = form.save(commit=False)
        page.save()
        messages.success(self.request, 'Данные обновлены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# pages end


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
