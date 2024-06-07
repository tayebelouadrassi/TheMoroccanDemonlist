from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import ClassicLevel, PlatformerLevel

# Register your models here.

class ClassicLevelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('ranking', 'name', 'points', 'min_points', 'min_completion', 'first_victor')
    ordering = ('ranking',)

admin.site.register(ClassicLevel, ClassicLevelAdmin)

class PlatformerLevelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('ranking', 'name', 'points', 'record_holder')
    ordering = ('ranking',)

admin.site.register(PlatformerLevel, PlatformerLevelAdmin)