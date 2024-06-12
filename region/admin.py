from django.contrib import admin
from .models import Region

# Register your models here.

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'classic_points', 'platformer_points')
    search_fields = ['name']

admin.site.register(Region, RegionAdmin)