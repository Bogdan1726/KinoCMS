from django.urls import path
from .views import *

urlpatterns = [
    # home page
    path('', HomePageView.as_view(), name='main'),
    # end
    path('poster/', PosterPageView.as_view(), name='poster'),

    path('soon/', SoonPageView.as_view(), name='soon'),

    path('movie_card/', get_movie_card, name='movie_card'),
    path('about_cinema/', get_about_cinema, name='about_cinema'),
    path('contacts/', get_contacts, name='contacts'),
    path('cafe_bar/', get_cafe_bar, name='cafe_bar'),
    path('children_room/', get_children_room, name='children_room'),
    path('news/', get_news, name='news'),
    path('vip/', get_vip, name='vip'),
    path('advertising/', get_advertising, name='advertising'),
    path('mobile_application/', get_mobile_application, name='mobile'),

]
