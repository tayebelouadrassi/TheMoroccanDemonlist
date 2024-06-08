from django.shortcuts import render
from .models import ClassicLevel, PlatformerLevel
from region.models import Region
from player.models import Player

# Create your views here.

def detail(request, pk):
    level = ClassicLevel.objects.get(pk=pk)
    total_records = level.classiclevelrecord_set.count()
    perfect_records = level.classiclevelrecord_set.filter(record_percentage=100).count()
    context = {
        'level': level,
        'total_records': total_records,
        'perfect_records': perfect_records
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