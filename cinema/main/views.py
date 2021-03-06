import json
from datetime import timedelta

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
from cms.models import HomePageBanner, CarouselBanner, PromotionsPageBanner, BackgroundBanner, Movies, HomePage, Seance, \
    Cinema, Halls, Images, Ticket, SeoBlock, Events, ContactsPage, Page


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
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
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
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
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
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()
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
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()

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
        time = datetime.now().time()
        context = super(ScheduleView, self).get_context_data()
        context['today'] = today
        context['home_page_data'] = HomePage.objects.all().first()
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
        context['week'] = [datetime.now() + timedelta(days=day) for day in range(7)]
        context['cinemas'] = Cinema.objects.all()
        context['movies'] = Movies.objects.all()
        context['seances'] = Seance.objects.select_related('movies', 'halls').filter(
            date=today, time__gt=time).order_by('time')
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
        time = datetime.now().time()
        hall = request.GET.get('hall') or False
        type_3d = True if request.GET.get('3d') else False
        type_2d = True if request.GET.get('2d') else False
        type_imax = True if request.GET.get('imax') else False
        movie = request.GET.get('movie') or False
        cinema = request.GET.get('cinema') or False
        date = request.GET.get('date') or datetime.now().date()
        halls = Halls.objects.values('id', 'number').none()
        seances = Seance.objects.select_related('movies', 'halls').filter(date=date).order_by('time')
        if date == datetime.now().date() or date == str(datetime.now().date()):
            seances = seances.filter(time__gt=time)
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
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()

        return context


class CinemasPageDetailView(DetailView):
    model = Cinema
    template_name = 'main/pages/cinemas/cinema_card.html'
    context_object_name = 'cinema'

    def get_context_data(self, **kwargs):
        halls_id = []
        date = datetime.now()
        context = super(CinemasPageDetailView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['halls'] = Halls.objects.filter(cinemas_id=self.object.id)
        context['images'] = Images.objects.filter(gallery_id=self.object.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()

        for hall in context['halls']:
            halls_id.append(hall.id)
        context['seances'] = Seance.objects.select_related(
            'movies', 'halls').filter(halls_id__in=halls_id, date=date).distinct('movies')[:5]
        return context


class HallPageDetailView(DetailView):
    model = Halls
    template_name = 'main/pages/cinemas/hall_card.html'
    context_object_name = 'hall'

    def get_context_data(self, **kwargs):
        date = datetime.now()
        context = super(HallPageDetailView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()
        context['images'] = Images.objects.filter(gallery_id=self.object.gallery_id)
        context['seances'] = Seance.objects.select_related(
            'movies', 'halls').filter(halls_id=self.object.id, date=date).distinct('movies')[:5]
        return context


# Cinemas end


# Promotions

class PromotionsPageView(ListView):
    model = Events
    template_name = 'main/pages/promotions/list_promotions.html'
    context_object_name = 'promotions'

    def get_queryset(self):
        return self.model.objects.filter(type='promotions').order_by('date_published')

    def get_context_data(self, **kwargs):
        context = super(PromotionsPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
        return context


class PromotionsDetailView(DetailView):
    model = Events
    template_name = 'main/pages/promotions/card_promotion.html'
    context_object_name = 'promotion'

    def get_context_data(self, **kwargs):
        context = super(PromotionsDetailView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=self.object.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()

        return context


# Promotions end

# News

class NewsPageView(ListView):
    model = Events
    template_name = 'main/pages/news/list_news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return self.model.objects.filter(type='news').order_by('date_published')

    def get_context_data(self, **kwargs):
        context = super(NewsPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
        return context


class NewsDetailView(DetailView):
    model = Events
    template_name = 'main/pages/news/card_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=self.object.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=self.object.seo_block_id).first()
        return context


# News end


# About cinema
class ContactsPageView(ListView):
    model = ContactsPage
    template_name = 'main/pages/about_cinema/contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return self.model.objects.filter(active=True).order_by('id')

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(ContactsPage, id=1)
        context = super(ContactsPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        context['api_key'] = settings.API_KEY
        return context


class AboutCinemaPageView(ListView):
    model = Page
    template_name = 'main/pages/about_cinema/about_cinema.html'
    context_object_name = 'cinema'

    def get_queryset(self):
        return self.model.objects.filter(is_base=True, id=2).first()

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(Page, id=2, is_base=True)
        context = super(AboutCinemaPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=objects.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        return context


class ChildrenRoomPageView(ListView):
    model = Page
    template_name = 'main/pages/about_cinema/children_room.html'
    context_object_name = 'children_room'

    def get_queryset(self):
        return self.model.objects.filter(is_base=True, id=6).first()

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(Page, id=6, is_base=True)
        context = super(ChildrenRoomPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=objects.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        return context


class VipHallPageView(ListView):
    model = Page
    template_name = 'main/pages/about_cinema/vip.html'
    context_object_name = 'vip'

    def get_queryset(self):
        return self.model.objects.filter(is_base=True, id=4).first()

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(Page, id=4, is_base=True)
        context = super(VipHallPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=objects.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        return context


class CafePageView(ListView):
    model = Page
    template_name = 'main/pages/about_cinema/cafe_bar.html'
    context_object_name = 'cafe'

    def get_queryset(self):
        return self.model.objects.filter(is_base=True, id=3).first()

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(Page, id=3, is_base=True)
        context = super(CafePageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=objects.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        return context


class AdvertisingPageView(ListView):
    model = Page
    template_name = 'main/pages/about_cinema/advertising.html'
    context_object_name = 'advertising'

    def get_queryset(self):
        return self.model.objects.filter(is_base=True, id=5).first()

    def get_context_data(self, **kwargs):
        objects = get_object_or_404(Page, id=5, is_base=True)
        context = super(AdvertisingPageView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        context['images'] = Images.objects.filter(gallery_id=objects.gallery_id)
        context['seo_block'] = SeoBlock.objects.filter(id=objects.seo_block_id).first()
        return context


class MobileApplicationPageView(ListView):

    def get(self, request, *args, **kwargs):
        return render(request, 'main/pages/about_cinema/mobile_application.html')

# About cinema end
