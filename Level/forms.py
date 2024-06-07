from django import forms
from .models import ClassicLevel

class ClassicLevelForm(forms.ModelForm):
    class Meta:
        model = ClassicLevel
        fields = ['id', 'name', 'publisher', 'difficulty', 'youtube_link', 'youtube_thumbnail', 'duration', 'min_completion', 'first_victor']
