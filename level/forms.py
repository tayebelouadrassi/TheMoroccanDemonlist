from django import forms

class LevelSearchForm(forms.Form):
    query = forms.CharField(max_length=255)