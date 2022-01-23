from django.urls import path
from .views import *

urlpatterns = [
    path('', statistics, name='cms'),
    path('list_movie/', list_movie, name='list_movie'),
    path('page_movie/', page_movie, name='page_movie'),
    path('banners/', banners, name='banners'),
    path('cinemas/', cinemas, name='cinemas'),
    path('news/', news, name='news'),
    path('promotions/', promotions, name='promotions'),
    path('pages/', pages, name='pages'),
    path('users/', CmsUserListView.as_view(), name='users'),
    path('users/edit/<int:pk>/', CmsUserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', CmsUserDeleteView.as_view(), name='user_delete'),
    path('mailing/', mailing, name='mailing')






]
