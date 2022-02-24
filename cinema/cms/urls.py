from django.urls import path
from .views import *

urlpatterns = [
    path('', statistics, name='cms'),
    path('list_movie/', list_movie, name='list_movie'),
    path('page_movie/', page_movie, name='page_movie'),
    path('banners/', banners, name='banners'),



    # cinemas
    path('cinemas/', CmsCinemasListView.as_view(), name='cinemas'),
    path('cinemas/create/', CmsCinemasCreateView.as_view(), name='cinemas_add'),
    path('cinemas/update/<int:pk>/', CmsCinemasUpdateView.as_view(), name='cinemas_edit'),
    path('cinemas/halls/create/<int:pk>/', CmsHallsCreateView.as_view(), name='halls_add'),
    path('cinemas/halls/delete/<int:pk>/', CmsHallsDeleteView.as_view(), name='halls_delete'),
    path('cinemas/halls/update/<int:pk>/', CmsHallsUpdateView.as_view(), name='halls_edit'),
    # cinemas end


    # news
    path('news/', CmsNewsListView.as_view(), name='news'),
    path('news/create/', CmsEventsCreateView.as_view(), name='news_add'),
    # news end

    # promotions
    path('promotions/', CmsPromotionListView.as_view(), name='promotions'),
    path('promotions/create/', CmsEventsCreateView.as_view(), name='promotions_add'),
    path('promotions/delete/<int:pk>/', CmsEventsDeleteView.as_view(), name='events_delete'),
    path('promotions/edit/<int:pk>/', CmsEventsUpdateView.as_view(), name='events_edit'),
    # promotions end

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
