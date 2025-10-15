from django.urls import path
from .views import *

urlpatterns = [

    path('breeds/search/', BreedSearchView.as_view(), name='breed-search'),
    path('breeds/favorites/', FavoriteBreedView.as_view(), name='favorite-breeds'),
    path('breeds/favorites/<str:breed_id>/', FavoriteBreedDetailView.as_view(), name='favorite-breed-detail'),


]