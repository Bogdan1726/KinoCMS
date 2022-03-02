from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from user.forms import UserUpdateForm
from user.models import User
from .forms import CmsHallsForm, CmsCinemasForm, CmsHomePageUpdateForm, \
    CmsPageUpdateForm, CmsContactsPageUpdateForm, \
    CmsEventsForm, CmsImageForm, CmsSeoBlockForm, CmsMoviesForm
from .models import SeoBlock, Gallery, Images, HomePageBanner, PromotionsPageBanner, \
    BackgroundBanner, Movies, Cinema, Halls, Seance, Ticket, Events, Page, HomePage, ContactsPage


# Create your views here.

# Base class
class BaseCmsUpdate(UpdateView):
    """
    Base view for updating an existing object.

    Using this base class requires subclassing to provide a response mixin.

    """

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if 'gallery_formset' in context:
            gallery_formset = context['gallery_formset']
            if seo_block_form.is_valid() and gallery_formset.is_valid():
                seo_block_form.save()
                obj = form.save(commit=False)
                for image in gallery_formset:
                    if image.cleaned_data:
                        if image.is_valid():
                            images = image.save(commit=False)
                            images.gallery = obj.gallery
                            images.save()
                gallery_formset.save()
                obj.save()
                messages.success(self.request, 'Данные обновлены')
                return super().form_valid(form)
            return self.form_invalid(form)
        else:
            if seo_block_form.is_valid():
                seo_block_form.save()
                obj = form.save(commit=False)
                obj.save()
                messages.success(self.request, 'Данные обновлены')
                return super().form_valid(form)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class BaseCmsCreate(CreateView):

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)

# Base class end

# movies


class CmsMoviesListView(ListView):
    model = Movies
    template_name = 'cms/pages/movies/list_movie.html'

    def get_queryset(self):
        movies = self.model.objects.filter(date_premier__lte=datetime.today())
        movies_coming_soon = self.model.objects.filter(date_premier__gt=datetime.today())
        queryset = {
            'movies': movies,
            'movies_coming_soon': movies_coming_soon
        }
        return queryset


class CmsMoviesUpdateView(BaseCmsUpdate):
    model = Movies
    template_name = 'cms/pages/movies/update_movie.html'
    form_class = CmsMoviesForm
    success_url = reverse_lazy('list_movie')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsMoviesUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))

        return context


class CmsMoviesCreateView(BaseCmsCreate):
    model = Movies
    template_name = 'cms/pages/movies/create_movie.html'
    form_class = CmsMoviesForm
    success_url = reverse_lazy('list_movie')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsMoviesCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            movie = form.save(commit=False)
            movie.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=movie.title)
            movie.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = movie.gallery
                        images.save()
            gallery_formset.save()
            movie.save()
            messages.success(self.request, 'Добавлен новый фильм')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsMoviesDeleteView(DeleteView):
    """
    Delete movie
    """
    model = Movies

    def get_success_url(self):
        messages.success(self.request, f'Фильм  {self.object.title} удалён!')
        return reverse_lazy('list_movie')

# movies end

# cinemas


class CmsCinemasListView(ListView):
    model = Cinema
    context_object_name = 'cinemas'
    template_name = 'cms/pages/cinemas/list_cinemas.html'

    def get_queryset(self):
        return super(CmsCinemasListView, self).get_queryset().order_by('id')


class CmsCinemasUpdateView(BaseCmsUpdate):
    model = Cinema
    template_name = 'cms/pages/cinemas/update_cinemas.html'
    form_class = CmsCinemasForm
    success_url = reverse_lazy('cinemas')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsCinemasUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))
        context['list_halls'] = Halls.objects.filter(cinemas=self.object).order_by('id')
        context['cinemas_id'] = self.object.id
        return context


class CmsCinemasCreateView(BaseCmsCreate):
    model = Cinema
    template_name = 'cms/pages/cinemas/create_cinemas.html'
    success_url = reverse_lazy('cinemas')
    form_class = CmsCinemasForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsCinemasCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            cinemas = form.save(commit=False)
            cinemas.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=cinemas.title)
            cinemas.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = cinemas.gallery
                        images.save()
            gallery_formset.save()
            cinemas.save()
            messages.success(self.request, 'Добавлен новый кинотеатр')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsCinemasDeleteView(DeleteView):
    """
    Delete cinemas
    """
    model = Cinema

    def get_success_url(self):
        messages.success(self.request, f'Кинотеатр  {self.object.title} удалён!')
        return reverse_lazy('cinemas')

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Объект защищен от удаления!')
        return redirect('cinemas')

# cinemas end

# halls


class CmsHallsCreateView(BaseCmsCreate):
    """
    Create Halls
    """
    model = Halls
    template_name = 'cms/pages/halls/create_halls.html'
    form_class = CmsHallsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHallsCreateView, self).get_context_data()
        context['cinemas_id'] = self.kwargs.get('pk')
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            halls = form.save(commit=False)
            halls.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=f"Зал-{halls.number}")
            halls.gallery = get_object_or_404(Gallery, id=gallery.id)
            halls.cinemas = get_object_or_404(Cinema, id=self.kwargs.get('pk'))
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = halls.gallery
                        images.save()
            gallery_formset.save()
            halls.save()
            messages.success(self.request, 'Добавлен новый зал')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsHallsUpdateView(BaseCmsUpdate):
    model = Halls
    template_name = 'cms/pages/halls/update_halls.html'
    form_class = CmsHallsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('cinemas_id')})

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHallsUpdateView, self).get_context_data()
        context['cinemas_id'] = self.kwargs.get('cinemas_id')
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))
        return context


class CmsHallsDeleteView(DeleteView):
    """
    Delete halls
    """
    model = Halls

    def get_success_url(self):
        messages.success(self.request, f'Зал № {self.object.number} удалён!')
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('cinemas_id')})

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Объект защищен от удаления!')
        return redirect('cinemas')

# halls end

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


class CmsHomePageUpdateView(BaseCmsUpdate):
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


class CmsPageUpdateView(BaseCmsUpdate):
    """
    Update a CMS pages
    """
    model = Page
    template_name = 'cms/pages/page/other_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsPageUpdateForm
    formset = modelformset_factory(ContactsPage, form=CmsContactsPageUpdateForm, extra=0)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPageUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))

        return context


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
        return self.form_invalid(form)

    def form_invalid(self, form):
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


class CmsEventsCreateView(BaseCmsCreate):
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
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
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
        return self.form_invalid(form)


class CmsEventsUpdateView(BaseCmsUpdate):
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


def index(request):
    return render(request, 'cms/elements/base.html')


def statistics(request):
    return render(request, 'cms/pages/statistics.html')


def banners(request):
    return render(request, 'cms/pages/banners.html')


def mailing(request):
    return render(request, 'cms/pages/mailing/mailing.html')
