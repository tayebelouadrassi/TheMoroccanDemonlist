from django.shortcuts import render, redirect
from .models import ClassicLevel, PlatformerLevel
from .forms import ClassicLevelForm

# Create your views here.

def add_classic_level(request):
    if request.method == 'POST':
        form = ClassicLevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Level:classic_mainlist')
    else:
        form = ClassicLevelForm()
    return render(request, 'level/classic/add.html', {'form': form})

def classic_mainlist(request):
    mainlist_levels = ClassicLevel.objects.filter(ranking__lte=75)
    context = {
        'mainlist_levels': mainlist_levels
    }
    return render(request, 'level/classic/mainlist.html', context)