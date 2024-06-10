from django.shortcuts import render
from .models import ClassicLevel, PlatformerLevel
from region.models import Region
from player.models import Player
from .forms import LevelSearchForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def search(request):
    if request.method == 'POST':
        form = LevelSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            classic_levels = ClassicLevel.objects.filter(name__icontains=query)
            platformer_levels = PlatformerLevel.objects.filter(name__icontains=query)
            levels = list(classic_levels) + list(platformer_levels)
            if len(levels) == 1:
                level = levels[0]
                if isinstance(level, ClassicLevel):
                    return redirect(reverse('level:classic_level_detail', args=[level.id]))
            else:
                return render(request, 'level/search.html', {'levels': levels})
        else:
            messages.error(request, ("No levels found. Please try again."))
            return redirect("level:classic_mainlist")

def detail(request, pk):
    level = ClassicLevel.objects.get(pk=pk)
    total_records = level.classiclevelrecord_set.count()
    perfect_records = level.classiclevelrecord_set.filter(record_percentage=100).count()
    youtube_id = level.youtube_link.split('.be/')[-1]
    staff_members = Player.objects.filter(is_staff=True)
    context = {
        'level': level,
        'total_records': total_records,
        'perfect_records': perfect_records,
        'youtube_id': youtube_id,
        'staff_members': staff_members
    }
    return render(request, 'level/classic/detail.html', context)

def classic_mainlist(request):
    mainlist_levels = ClassicLevel.objects.filter(ranking__lte=75)
    context = {
        'mainlist_levels': mainlist_levels
    }
    return render(request, 'level/classic/mainlist.html', context)

def classic_extendedlist(request):
    extended_levels = ClassicLevel.objects.filter(ranking__range=(76, 150))
    context = {
        'extended_levels': extended_levels
    }
    return render(request, 'level/classic/extendedlist.html', context)

def classic_legacylist(request):
    legacy_levels = ClassicLevel.objects.filter(ranking__gt=150)
    context = {
        'legacy_levels': legacy_levels
    }
    return render(request, 'level/classic/legacylist.html', context)

def classic_stat_viewer(request):
    regions = Region.objects.all()
    for region in regions:
        region.players = Player.objects.filter(region=region)
    return render(request, 'level/classic/statviewer.html', {'regions': regions})