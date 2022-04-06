import json
from datetime import timedelta

from babel.dates import format_date
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
from cms.models import HomePageBanner, CarouselBanner, PromotionsPageBanner, BackgroundBanner, Movies, HomePage, Seance, \
    Cinema


# Create your views here.

# Home page


class HomePageView(ListView):

    def get(self, request, *args, **kwargs):
        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        movies = Movies.objects.all()
        context = {
            'today': today,
            'list_movie_today':
                Seance.objects.filter(date=today).select_related('movies').distinct('movies'),
            'list_movie_premier': movies.filter(date_premier__range=[today, today + timedelta(days=7)]),
            'list_movie_soon': movies.filter(date_premier__gt=today).order_by('date_premier'),
            'home_page_data': HomePage.objects.all().first(),

            'promotion_banner': PromotionsPageBanner.objects.all(),
            'background': BackgroundBanner.objects.all().first(),
            'header_banner': HomePageBanner.objects.all(),
            'banner_carousel': CarouselBanner.objects.filter(value='home_page_banner').first(),
            'promotion_carousel': CarouselBanner.objects.filter(value='promotions_page_banner').first()
        }
        return render(request, 'main/pages/home/index.html', context)


# Home page end


# Poster page

class PosterPageView(ListView):

    def get(self, request, *args, **kwargs):
        today = datetime.now()

        context = {
            'list_movies':
                Seance.objects.filter(date=today).select_related('movies').distinct('movies'),
            'home_page_data': HomePage.objects.all().first(),

        }
        return render(request, 'main/pages/poster/poster.html', context)


# Poster page end

# Soon page

class SoonPageView(ListView):

    def get(self, request, *args, **kwargs):
        today = datetime.now()

        context = {
            'list_movie_soon': Movies.objects.filter(date_premier__gt=today).order_by('date_premier'),
            'home_page_data': HomePage.objects.all().first(),

        }
        return render(request, 'main/pages/poster/soon.html', context)

# Soon page end


# Movie card

class MovieCard(DetailView):
    model = Movies
    template_name = 'main/pages/movie_card.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super(MovieCard, self).get_context_data()
        context['week'] = [datetime.now() + timedelta(days=day) for day in range(7)]
        context['cinemas'] = Cinema.objects.all()
        return context


def card_movie_ajax(request):
    if request.is_ajax():
        date = request.GET.get('day')
        type_seance = request.GET.get('type')
        list_seance = list(Seance.objects.filter(date=date).
                           values('time', 'ticket_price', 'halls__number', 'movies'))
        print(list_seance)
        response = {
            'list_seance': list_seance
        }
        return JsonResponse(response, status=200)
    return HttpResponse(request)


# Movie car end



def get_about_cinema(request):
    return render(request, 'main/pages/about_cinema/about_cinema.html')


def get_contacts(request):
    return render(request, 'main/pages/about_cinema/contacts.html')


def get_cafe_bar(request):
    return render(request, 'main/pages/about_cinema/cafe_bar.html')


def get_children_room(request):
    return render(request, 'main/pages/about_cinema/children_room.html')


def get_news(request):
    return render(request, 'main/pages/about_cinema/news.html')


def get_vip(request):
    return render(request, 'main/pages/about_cinema/vip.html')


def get_advertising(request):
    return render(request, 'main/pages/about_cinema/advertising.html')


def get_mobile_application(request):
    return render(request, 'main/pages/about_cinema/mobile_application.html')
