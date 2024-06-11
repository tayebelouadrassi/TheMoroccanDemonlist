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

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 50:
            raise forms.ValidationError("Comment cannot exceed 50 characters.")
        return comment
    
    def clean_record_percentage(self):
        record_percentage = self.cleaned_data['record_percentage']
        level = self.cleaned_data.get('level')
        if level and record_percentage < level.min_completion:
            raise forms.ValidationError("Your record percentage is lower than the minimum requirement of that level.")
        return record_percentage

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

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 50:
            raise forms.ValidationError("Comment cannot exceed 50 characters.")
        return comment