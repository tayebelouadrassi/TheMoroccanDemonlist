from django import forms
from .models import ClassicRecordSubmission, PlatformerRecordSubmission
    
class ClassicRecordSubmissionForm(forms.ModelForm):
    class Meta:
        model = ClassicRecordSubmission
        fields = ['level', 'record_link', 'record_percentage', 'comment']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'record_link': forms.URLInput(attrs={'class': 'form-control'}),
            'record_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PlatformerRecordSubmissionForm(forms.ModelForm):
    class Meta:
        model = PlatformerRecordSubmission
        fields = ['level', 'record_link', 'record_time', 'comment']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'record_link': forms.URLInput(attrs={'class': 'form-control'}),
            'record_time': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
