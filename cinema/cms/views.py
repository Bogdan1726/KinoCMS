from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from user.forms import UserUpdateForm
from user.models import User


# Create your views here.

class CmsUserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'cms/pages/users/list_users.html'


class CmsUserUpdateView(UpdateView):
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
    model = User
    success_url = reverse_lazy('users')
    template_name = 'cms/pages/users/list_users.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.success(request, 'Пользователь удалён!')
            return self.delete(request, *args, **kwargs)
        messages.warning(request, 'Для удаления пользователей нужно иметь права администратора')
        return redirect('users')


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


def pages(request):
    return render(request, 'cms/pages/page/list_pages.html')


def mailing(request):
    return render(request, 'cms/pages/mailing/mailing.html')
