from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import ClassicLevel, PlatformerLevel
import math
from pytube import YouTube

# Register your models here.

class CustomSortableAdminMixin(SortableAdminMixin):
    def _update_order(self, updated_items, extra_model_filters):
        super()._update_order(updated_items, extra_model_filters)
        for item in updated_items:
            if ClassicLevel.objects.filter(pk=item[0]).exists():
                level = ClassicLevel.objects.get(pk=item[0])
                level.save()
                for level_record in level.classiclevelrecord_set.all():
                    level_record.save()
            if PlatformerLevel.objects.filter(pk=item[0]).exists():
                level = PlatformerLevel.objects.get(pk=item[0])
                level.save()
                for level_record in level.platformerlevelrecord_set.all():
                    level_record.save()

class ClassicLevelAdmin(CustomSortableAdminMixin, admin.ModelAdmin):
    list_display = ['ranking', 'name', 'points', 'min_points', 'min_completion', 'first_victor']
    ordering = ['ranking']
    exclude = ['points', 'min_points', 'youtube_thumbnail']
    actions = ['save_all']

    def save_model(self, request, obj, form, change):
        id = form.cleaned_data.get('id')
        youtube_link = form.cleaned_data.get('youtube_link')

        if id and youtube_link:
            try:
                obj.youtube_thumbnail = YouTube(youtube_link).thumbnail_url
            except Exception as e:
                pass

        super().save_model(request, obj, form, change)

    def save_all(self, request, queryset):
        for obj in queryset:
            obj.points = round(500 * (1 - math.log(obj.ranking, 151)), 2)
            obj.min_points = round((500 * (1 - math.log(obj.ranking, 151))) * 1/3, 2)
            obj.save()

            for level_record in obj.classiclevelrecord_set.all():
                level_record.save()

        self.message_user(request, f"{queryset.count()} levels saved successfully.")

    save_all.short_description = "Save selected levels"

admin.site.register(ClassicLevel, ClassicLevelAdmin)

class PlatformerLevelAdmin(CustomSortableAdminMixin, admin.ModelAdmin):
    list_display = ['ranking', 'name', 'points', 'record_holder']
    ordering = ['ranking']
    exclude = ['points', 'youtube_thumbnail']
    actions = ['save_all']

    def save_model(self, request, obj, form, change):
        id = form.cleaned_data.get('id')
        youtube_link = form.cleaned_data.get('youtube_link')

        if id and youtube_link:
            try:
                obj.youtube_thumbnail = YouTube(youtube_link).thumbnail_url
            except Exception as e:
                pass

        super().save_model(request, obj, form, change)

    def save_all(self, request, queryset):
        for obj in queryset:
            obj.points = round(500 * (1 - math.log(obj.ranking, 151)), 2)
            obj.save()

            for level_record in obj.levelrecord_set.all():
                level_record.save()

        self.message_user(request, f"{queryset.count()} levels saved successfully.")

    save_all.short_description = "Save selected levels"

admin.site.register(PlatformerLevel, PlatformerLevelAdmin)