from django.contrib import admin
from .models import ClassicLevelRecord, PlatformerLevelRecord

# Register your models here.


class ClassicLevelRecordAdmin(admin.ModelAdmin):
    list_display = ('level', 'player', 'record_link', 'record_percentage')
    search_fields = ['level', 'player']

admin.site.register(ClassicLevelRecord, ClassicLevelRecordAdmin)

class PlatformerLevelRecordAdmin(admin.ModelAdmin):
    list_display = ('level', 'player', 'record_link', 'record_time')
    search_fields = ['level', 'player']

admin.site.register(PlatformerLevelRecord, PlatformerLevelRecordAdmin)