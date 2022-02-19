from django.urls import path
from .views import *

urlpatterns = [
    path('', statistics, name='cms'),
    path('list_movie/', list_movie, name='list_movie'),
    path('page_movie/', page_movie, name='page_movie'),
    path('banners/', banners, name='banners'),
    path('cinemas/', cinemas, name='cinemas'),
    path('news/', news, name='news'),

    # promotions
    path('promotions/', CmsPromotionListView.as_view(), name='promotions'),
    path('promotions/create/', CmsPromotionCreateView.as_view(), name='promotions_add'),
    path('promotions/delete/<int:pk>/', CmsPromotionDeleteView.as_view(), name='promotions_delete'),
    path('promotions/edit/<int:pk>/', CmsPromotionsUpdateView.as_view(), name='promotions_edit'),
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
