from django.shortcuts import render, redirect
from .forms import RegisterForm, ReviewForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import requests
from .models import Review, WatchList, Movie


def home(request):
    return render(request, 'movies_app/home.html')



def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Succesfully! Login now.')
            return redirect('/login')
        else:
            form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required(login_url='/login')
def movies(request):
    url = 'https://api.themoviedb.org/3/discover/movie'
    params = {'api_key': 'bf3ce5fa7c0e31adaa82cb21e0c6886e', 'page': 100}
    response = requests.get(url, params=params)
    data = response.json()
    movies = data['results']
    if request.method == 'POST':
        user = request.user
        movie = request.POST.get('movie')

        # Get the user's watchlist or create a new one if it doesn't exist
        watchlist, created = WatchList.objects.get_or_create(user=user)

        # Create a new movie object and add it to the user's watchlist
        title = Movie(title=movie)
        title.save()
        watchlist.movies.add(title)
        messages.success(request, 'Movie Added to Watchlist.')
        return render(request, 'movies_app/movies.html', {'movies': movies})

    return render(request, 'movies_app/movies.html', {'movies': movies})



@login_required(login_url='/login')
def movie_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        url = f'https://api.themoviedb.org/3/search/movie?api_key=bf3ce5fa7c0e31adaa82cb21e0c6886e&query={query}'
        response = requests.get(url)
        results = response.json()['results']
        context = {'results': results, 'query': query}
        # user = request.user
        # movie = request.POST.get('movie')
        # to check if watchlist button is clicked
        if 'add_to_watchlist' in request.POST:
            user = request.user
            movie = request.POST.get('movie')

            # Get the user's watchlist or create a new one if it doesn't exist
            watchlist, created = WatchList.objects.get_or_create(user=user)

            # Create a new movie object and add it to the user's watchlist
            title = Movie(title=movie)
            title.save()
            watchlist.movies.add(title)

        return render(request, 'movies_app/search.html', context)
    
    else:
        return render(request, 'movies_app/search.html')
    




@login_required(login_url='/login')
def reviews(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    else:
        form = ReviewForm()
    return render(request, 'movies_app/reviews.html', {'form': form})



@login_required(login_url='/login')
def watchlist(request):
    user = request.user
    movies_list = WatchList.objects.filter(user=user).first()
    
    if movies_list is not None:
        movies = movies_list.movies.all()
    else:
        movies = []

    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        movies_list.movies.remove(movie_obj)

    return render(request, 'movies_app/watchlist.html', {'movies': movies})
