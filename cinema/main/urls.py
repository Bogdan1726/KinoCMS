from django.urls import path
from .views import *

urlpatterns = [
    # home page
    path('', HomePageView.as_view(), name='main'),
    # end

    # movies
    path('poster/', PosterPageView.as_view(), name='poster'),
    path('soon/', SoonPageView.as_view(), name='soon'),
    path('movie_card/<int:pk>/', MovieCard.as_view(), name='movie_card'),
    path('movie_card/seance_filter/', card_movie_ajax, name='seance_filter'),
    # movies end

    # ticket
    path('ticket_booking/<int:pk>/<int:seance_id>/', TicketBookingView.as_view(), name='ticket_booking'),
    path('ticket/', ticket_selected, name='ticket_selected'),
    path('ticket_buy/', ticket_buy_booking, name='ticket_buy_booking'),
    # ticket end

    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('schedule_filter/', filter_seances, name='filter_seances'),

    # cinemas
    path('cinemas/', CinemasPageView.as_view(), name='list_cinemas'),
    path('cinemas/<int:pk>/', CinemasPageDetailView.as_view(), name='cinema_card'),
    path('cinemas/halls/<int:pk>/', HallPageDetailView.as_view(), name='hall_card'),
    # cinemas end

    # promotions
    path('promotions/', PromotionsPageView.as_view(), name='main_promotion'),
    path('promotions/<int:pk>/', PromotionsDetailView.as_view(), name='promotion_card'),
    # promotions end

    # news
    path('news/', NewsPageView.as_view(), name='main_news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_card'),
    # news end

    # about cinema
    path('about_cinema/', AboutCinemaPageView.as_view(), name='about_cinema'),
    path('about_cinema/contacts/', ContactsPageView.as_view(), name='main_contacts'),
    path('about_cinema/children_room/', ChildrenRoomPageView.as_view(), name='children_room'),
    path('about_cinema/vip/', VipHallPageView.as_view(), name='vip'),
    path('about_cinema/cafe_bar/', CafePageView.as_view(), name='cafe_bar'),
    path('about_cinema/advertising/', AdvertisingPageView.as_view(), name='advertising'),
    path('about_cinema/mobile_application/', MobileApplicationPageView.as_view(), name='mobile'),
    # about cinema end


]
