from django.contrib import admin
from .models import Player

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'region', 'classic_points', 'platformer_points', 'date_joined')
    search_fields = ['username']

admin.site.register(Player, PlayerAdmin)