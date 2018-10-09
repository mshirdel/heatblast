from django import forms
from .models import Item


class StoryForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'url', 'item_body_text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'item_body_text': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'عنوان',
            'url': 'آدرس لینک',
            'item_body_text': 'متن برای گفتگو'
        }
