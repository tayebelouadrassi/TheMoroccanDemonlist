from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Player
from django.contrib import messages
from .forms import PlayerCreationForm

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Player.objects.get(username=username)
        except Player.DoesNotExist:
            messages.error(request, "This user does not exist.")
            return redirect("player:login")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, ("Password is incorrect."))
            return redirect("player:login")
    else:
        return render(request, 'player/login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect("player:login")

def register_user(request):
    if request.method == "POST":
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful."))
            return redirect("home")
    else:
        form = PlayerCreationForm()

    context = {
        'form':form,
    }

    return render(request, 'player/register.html', context)