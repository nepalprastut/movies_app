from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=100)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_name + "\n" + self.review   


class Movie(models.Model):
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title



class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)


    def __str__(self):
        return self.user.username
    

