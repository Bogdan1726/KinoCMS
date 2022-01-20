from django.shortcuts import render
from django.views.generic import ListView

from user.models import User


# Create your views here.

class UserListView(ListView):
    model = User
    context_object_name = 'user'
    template_name = 'cms/pages/users/list_users.html'


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


