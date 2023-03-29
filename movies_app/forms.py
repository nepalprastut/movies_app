from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) # we added the email field here because Django's UserCreationForm class has only username and password fields

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie_name', 'review']


