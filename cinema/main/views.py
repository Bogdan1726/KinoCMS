import json
from datetime import timedelta
from itertools import chain

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
from cms.models import HomePageBanner, CarouselBanner, PromotionsPageBanner, BackgroundBanner, Movies, HomePage, Seance, \
    Cinema, Halls, Images, Ticket, SeoBlock


# Create your views here.

# Home page


class HomePageView(ListView):
    model = HomePage
    template_name = 'main/pages/home/index.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        movies = Movies.objects.all()
        context = super(HomePageView, self).get_context_data()
        context['today'] = today
        context['list_movie_today'] = Seance.objects.filter(date=today).select_related('movies').distinct('movies')
        context['list_movie_premier'] = movies.filter(date_premier__range=[today, today + timedelta(days=7)])
        context['list_movie_soon'] = movies.filter(date_premier__gt=today).order_by('date_premier')
        context['home_page_data'] = HomePage.objects.all().first()
        context['promotion_banner'] = PromotionsPageBanner.objects.all()
        context['background'] = BackgroundBanner.objects.all().first()
        context['header_banner'] = HomePageBanner.objects.all()
        context['banner_carousel'] = CarouselBanner.objects.filter(value='home_page_banner').first()
        context['promotion_carousel'] = CarouselBanner.objects.filter(value='promotions_page_banner').first()
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
        return context


# Home page end


# Poster page

class PosterPageView(ListView):
    model = Seance
    template_name = 'main/pages/poster/poster.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        context = super(PosterPageView, self).get_context_data()
        context['list_movies'] = self.model.objects.filter(date=today).select_related('movies').distinct('movies')
        context['home_page_data'] = HomePage.objects.all().first()
        return context


# Poster page end


# Soon page

class SoonPageView(ListView):
    model = Movies
    template_name = 'main/pages/poster/soon.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        context = super(SoonPageView, self).get_context_data()
        context['list_movie_soon'] = self.model.objects.filter(date_premier__gt=today).order_by('date_premier')
        context['home_page_data'] = HomePage.objects.all().first()
        return context


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
        context['images'] = Images.objects.filter(gallery_id=self.object.gallery_id)
        context['home_page_data'] = HomePage.objects.all().first()
        return context


# ajax
def card_movie_ajax(request):
    if request.is_ajax():
        halls_id = []
        seance = Seance.objects.all()
        time = datetime.now().time()
        date = request.GET.get('day')
        cinema_id = request.GET.get('cinema_id')
        type_seance = request.GET.get('type')
        movie_id = request.GET.get('movie_id')
        halls = Halls.objects.values('id', 'number').filter(cinemas_id=cinema_id)
        for hall in halls:
            halls_id.append(hall.get('id'))
        if date == str(datetime.now().date()):
            seance = seance.filter(date=date, time__gt=time)
        list_seance = seance.filter(movies_id=movie_id, date=date, halls_id__in=halls_id). \
            values('id', 'time', 'ticket_price', 'halls__number', 'movies', 'halls__id')
        if type_seance == 'imax':
            list_seance = list_seance.filter(movies__type_imax=True)
        if type_seance == '2d':
            list_seance = list_seance.filter(movies__type_2d=True).values()
        if type_seance == '3d':
            list_seance = list_seance.filter(movies__type_3d=True).values()
        response = {
            'list_seance': list(list_seance)
        }
        return JsonResponse(response, status=200)
    return HttpResponse()


# ajax end
# Movie car end


# Ticket Booking
class TicketBookingView(DetailView):
    template_name = 'main/pages/ticket_booking.html'
    model = Halls
    context_object_name = 'hall'

    def get_context_data(self, **kwargs):
        context = super(TicketBookingView, self).get_context_data()
        context['seance'] = Seance.objects.filter(id=self.kwargs.get('seance_id')).first()
        context['movie_image'] = Movies.objects.get(id=context['seance'].movies_id)
        context['home_page_data'] = HomePage.objects.all().first()
        return context


# ajax

def ticket_buy_booking(request):
    if request.is_ajax:
        type_ticket = request.GET.get('type')
        row = request.GET.get('row')
        place = request.GET.get('place')
        seance_id = request.GET.get('seance_id')
        if type_ticket == 'booking':
            Ticket.objects.create(
                row=row, place=place, type=True, seance_id=seance_id, user_id=request.user.id
            )
        else:
            Ticket.objects.create(
                row=row, place=place, type=False, seance_id=seance_id, user_id=request.user.id
            )
        response = {
        }
        return JsonResponse(response, status=200)
    return HttpResponse()


def ticket_selected(request):
    if request.is_ajax:
        seance_id = request.GET.get('seance_id')
        tickets = list(Ticket.objects.filter(seance_id=seance_id).values('row', 'place', 'type', 'user_id'))
        response = {
            'tickets': tickets
        }
        return JsonResponse(response, status=200)
    return HttpResponse()


# ajax end

# Ticket Booking end


# Schedule

class ScheduleView(ListView):
    model = Seance
    template_name = 'main/pages/schedule.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        context = super(ScheduleView, self).get_context_data()
        context['today'] = today
        context['home_page_data'] = HomePage.objects.all().first()
        context['week'] = [datetime.now() + timedelta(days=day) for day in range(7)]
        context['cinemas'] = Cinema.objects.all()
        context['movies'] = Movies.objects.all()
        context['seances'] = Seance.objects.select_related('movies', 'halls').filter(date=today).order_by('time')
        return context


def serializers_queryset(queryset):
    lists = []
    for obj in queryset:
        lists.append(
            {
                'model': 'Seances',
                'pk': obj.id,
                'fields': {
                    'time': obj.time,
                    'movies': obj.movies.title,
                    'halls': obj.halls.number,
                    'halls_id': obj.halls.id,
                    'ticket_price': obj.ticket_price,
                    'movies_id': obj.movies.id
                }
            }
        )
    return lists


def filter_seances(request):
    if request.is_ajax:
        hall = request.GET.get('hall') or False
        type_3d = True if request.GET.get('3d') else False
        type_2d = True if request.GET.get('2d') else False
        type_imax = True if request.GET.get('imax') else False
        movie = request.GET.get('movie') or False
        cinema = request.GET.get('cinema') or False
        date = request.GET.get('date') or datetime.now()
        halls = Halls.objects.values('id', 'number').none()
        seances = Seance.objects.select_related('movies', 'halls').filter(date=date).order_by('time')
        if type_3d:
            seances = seances.filter(movies__type_3d=True)
        if type_2d:
            seances = seances.filter(movies__type_2d=True)
        if type_imax:
            seances = seances.filter(movies__type_imax=True)
        if movie:
            seances = seances.filter(movies__id=movie)
        if hall:
            seances = seances.filter(halls_id=hall)
        if cinema:
            halls_id = []
            halls = Halls.objects.values('id', 'number').filter(cinemas_id=cinema)
            for hall in halls:
                halls_id.append(hall.get('id'))
            seances = seances.filter(halls_id__in=halls_id)
        response = {
            'seances': serializers_queryset(seances),
            'halls': list(halls)
        }
        return JsonResponse(response, status=200)
    return HttpResponse()


# Schedule end


# Cinemas

class CinemasPageView(ListView):
    model = Cinema
    template_name = 'main/pages/cinemas/list_cinemas.html'
    context_object_name = 'cinemas'

    def get_context_data(self, **kwargs):
        context = super(CinemasPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        return context


class CinemasPageDetailView(DetailView):
    model = Cinema
    template_name = 'main/pages/cinemas/cinema_card.html'
    context_object_name = 'cinema'

# Cinemas end

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
