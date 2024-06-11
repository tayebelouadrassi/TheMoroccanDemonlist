from django.contrib import admin
from .models import ClassicRecordSubmission, PlatformerRecordSubmission

# Register your models here.

class ClassicRecordSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'record_link', 'record_percentage', 'comment', 'submission_date', 'status')
    search_fields = ['id']

admin.site.register(ClassicRecordSubmission, ClassicRecordSubmissionAdmin)

class PlatformerRecordSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'record_link', 'record_time', 'comment', 'submission_date', 'status')
    search_fields = ['id']

admin.site.register(PlatformerRecordSubmission, PlatformerRecordSubmissionAdmin)