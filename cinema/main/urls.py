from django.urls import path
from .views import *

urlpatterns = [
    # home page
    path('', HomePageView.as_view(), name='main'),
    # end
    path('poster/', PosterPageView.as_view(), name='poster'),
    path('soon/', SoonPageView.as_view(), name='soon'),

    # movies
    path('movie_card/<int:pk>/', MovieCard.as_view(), name='movie_card'),
    path('movie_card/seance_filter/', card_movie_ajax, name='seance_filter'),
    # movies end

    # ticket
    path('ticket_booking/<int:pk>/<int:seance_id>/', TicketBookingView.as_view(), name='ticket_booking'),
    path('ticket/', ticket_selected, name='ticket_selected'),
    path('ticket_buy/', ticket_buy_booking, name='ticket_buy_booking'),
    # ticket end

    path('about_cinema/', get_about_cinema, name='about_cinema'),
    path('contacts/', get_contacts, name='contacts'),
    path('cafe_bar/', get_cafe_bar, name='cafe_bar'),
    path('children_room/', get_children_room, name='children_room'),
    path('news/', get_news, name='news'),
    path('vip/', get_vip, name='vip'),
    path('advertising/', get_advertising, name='advertising'),
    path('mobile_application/', get_mobile_application, name='mobile'),

]
