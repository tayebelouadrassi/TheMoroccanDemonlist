from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Player
        fields = ('username', 'email', 'password1', 'password2')