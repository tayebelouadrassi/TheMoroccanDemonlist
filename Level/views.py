from django.shortcuts import render
from .models import ClassicLevel, PlatformerLevel

# Create your views here.

def classic_mainlist(request):
    mainlist_levels = ClassicLevel.objects.filter(ranking__lte=75)
    context = {
        'mainlist_levels': mainlist_levels
    }
    return render(request, 'level/classic/mainlist.html', context)