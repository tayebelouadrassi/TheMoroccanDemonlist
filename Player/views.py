from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Player
from django.contrib import messages
from .forms import PlayerCreationForm
from levelrecord.models import ClassicLevelRecord
from django.db.models import Q

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

def profile(request, username):
    player = Player.objects.get(username=username)

    player_ranking = Player.objects.filter(classic_points__gt=player.classic_points).count() + 1
    beaten_levels = ClassicLevelRecord.objects.filter(player=player)
    hardest_level = beaten_levels.order_by('level__ranking').first()
    first_victors = [record for record in beaten_levels if record.level.first_victor == player]
    level_counts = {
      'main': beaten_levels.filter(level__ranking__lte=75).count(),
      'extended': beaten_levels.filter(Q(level__ranking__gt=75) & Q(level__ranking__lte=150)).count(),
      'legacy': beaten_levels.filter(level__ranking__gt=150).count()
    }

    context = {
        'player': player,
        'player_ranking': player_ranking,
        'beaten_levels': beaten_levels,
        'hardest_level': hardest_level,
        'first_victors': first_victors,
        'level_counts': level_counts,
    }

    return render(request, 'player/profile.html', context)