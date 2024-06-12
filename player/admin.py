from django.contrib import admin
from .models import Player

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'region', 'classic_points', 'platformer_points', 'date_joined', 'is_email_verified', 'is_staff')
    search_fields = ['username']

admin.site.register(Player, PlayerAdmin)