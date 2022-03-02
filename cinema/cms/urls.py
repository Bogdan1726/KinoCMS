from django.urls import path
from .views import *

urlpatterns = [
    path('', statistics, name='cms'),
    path('banners/', banners, name='banners'),

    # movies
    path('movies/', CmsMoviesListView.as_view(), name='list_movie'),
    path('movies/create/', CmsMoviesCreateView.as_view(), name='movies_add'),
    path('movies/update/<int:pk>/', CmsMoviesUpdateView.as_view(), name='movies_edit'),
    path('movies/delete/<int:pk>/', CmsMoviesDeleteView.as_view(), name='movies_delete'),

    # movies end


    # cinemas
    path('cinemas/', CmsCinemasListView.as_view(), name='cinemas'),
    path('cinemas/create/', CmsCinemasCreateView.as_view(), name='cinemas_add'),
    path('cinemas/update/<int:pk>/', CmsCinemasUpdateView.as_view(), name='cinemas_edit'),
    path('cinemas/delete/<int:pk>/', CmsCinemasDeleteView.as_view(), name='cinemas_delete'),
    path('cinemas/halls/create/<int:pk>/', CmsHallsCreateView.as_view(), name='halls_add'),
    path('cinemas/<int:cinemas_id>/halls/delete/<int:pk>/', CmsHallsDeleteView.as_view(), name='halls_delete'),
    path('cinemas/<int:cinemas_id>/halls/update/<int:pk>/', CmsHallsUpdateView.as_view(), name='halls_edit'),
    # cinemas end


    # news
    path('news/', CmsNewsListView.as_view(), name='news'),
    path('news/create/', CmsEventsCreateView.as_view(), name='news_add'),
    # news end

    # events
    path('promotions/', CmsPromotionListView.as_view(), name='promotions'),
    path('promotions/create/', CmsEventsCreateView.as_view(), name='promotions_add'),
    path('promotions/delete/<int:pk>/', CmsEventsDeleteView.as_view(), name='events_delete'),
    path('promotions/edit/<int:pk>/', CmsEventsUpdateView.as_view(), name='events_edit'),
    # events end

    # pages
    path('pages/', CmsPagesListView.as_view(), name='pages'),
    path('pages/home_page/<int:pk>/', CmsHomePageUpdateView.as_view(), name='home_page'),
    path('pages/page/<int:pk>/', CmsPageUpdateView.as_view(), name='page'),
    path('pages/contacts_page/<int:pk>/', CmsContactsUpdateView.as_view(), name='contact'),
    # pages end

    # users
    path('users/', CmsUserListView.as_view(), name='users'),
    path('users/edit/<int:pk>/', CmsUserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', CmsUserDeleteView.as_view(), name='user_delete'),
    # users end

    path('mailing/', mailing, name='mailing')

]
