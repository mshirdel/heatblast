from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'url', 'story_body_text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'story_body_text': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'عنوان',
            'url': 'آدرس لینک',
            'story_body_text': 'متن برای گفتگو'
        }
