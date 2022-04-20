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

    # about cinema
    path('news/', NewsPageView.as_view(), name='main_news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_card'),

    # about cinema end


    path('contacts/', get_contacts, name='contacts'),
    path('cafe_bar/', get_cafe_bar, name='cafe_bar'),
    path('children_room/', get_children_room, name='children_room'),
    path('news/', get_news, name='main_news'),
    path('vip/', get_vip, name='vip'),
    path('advertising/', get_advertising, name='advertising'),
    path('mobile_application/', get_mobile_application, name='mobile'),

]
