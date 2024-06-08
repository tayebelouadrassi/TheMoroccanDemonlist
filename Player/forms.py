from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player
from region.models import Region

class PlayerCreationForm(UserCreationForm):
    email = forms.EmailField()
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True)

    class Meta:
        model = Player
        fields = ('username', 'email', 'region', 'password1', 'password2')