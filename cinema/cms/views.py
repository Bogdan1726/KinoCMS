from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

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
        context['contacts_pages'] = ContactsPage.objects.all()[0]
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
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
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

    def get_success_url(self):
        return reverse_lazy('pages')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = modelformset_factory(ContactsPage, form=CmsContactsPageUpdateForm, extra=0)
        return form_class(self.request.POST or None,
                          self.request.FILES or None,
                          queryset=ContactsPage.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(CmsContactsUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if seo_block_form.is_valid():
            seo_block_form.save()
            for contacts in form:
                if contacts.cleaned_data:
                    if contacts.is_valid():
                        contacts = contacts.save(commit=False)
                        contacts.seo_block = seo_block_form.instance
                        contacts.save()
            form.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# pages end

# Events

class CmsPromotionListView(ListView):
    """
    list of promotion
    """
    model = Events
    context_object_name = 'promotions'
    template_name = 'cms/pages/promotions/list_promotions.html'


class CmsNewsListView(ListView):
    """
    list of news
    """
    model = Events
    context_object_name = 'news'
    template_name = 'cms/pages/news/list_news.html'


class CmsEventsCreateView(CreateView):
    """
    Create a new events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/create_events.html'
    form_class = CmsEventsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        url_request = self.request.get_full_path()
        if url_request == '/cms/promotions/create/':
            return reverse_lazy('promotions')
        else:
            return reverse_lazy('news')

    def get_context_data(self, *args, **kwargs):
        context = super(CmsEventsCreateView, self).get_context_data()
        context['get_path'] = self.request.get_full_path()
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
            if self.request.get_full_path() == '/cms/promotions/create/':
                promotion.type = 'promotions'
            else:
                promotion.type = 'news'
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


class CmsEventsUpdateView(UpdateView):
    """
    Update events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/update_events.html'
    form_class = CmsEventsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        type_events = self.object.type
        if type_events == 'promotions':
            return reverse_lazy('promotions')
        else:
            return reverse_lazy('news')

    def get_context_data(self, *args, **kwargs):
        context = super(CmsEventsUpdateView, self).get_context_data()
        context['type_object'] = self.object.type
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
            for image in formset_gallery:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = self.object.gallery
                        images.save()
            formset_gallery.save()
            seo_block_form.save()
            self.object = form.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
            return super().form_invalid(form)

    def form_invalid(self, form):
        print('invalid')
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsEventsDeleteView(DeleteView):
    """
    Delete events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/list_promotions.html'

    def get_success_url(self):
        type_events = self.object.type
        if type_events == 'promotions':
            messages.success(self.request, 'Акция удалена!')
            return reverse_lazy('promotions')
        else:
            messages.success(self.request, 'Новость удалена!')
            return reverse_lazy('news')

# Events end


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




def mailing(request):
    return render(request, 'cms/pages/mailing/mailing.html')
