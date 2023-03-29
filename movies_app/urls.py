from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('movies', views.movies, name='movies'),
    path('search', views.movie_search, name='search'),
    path('reviews', views.reviews, name='reviews'),
    path('watchlist', views.watchlist, name='watchlist'),
    
]