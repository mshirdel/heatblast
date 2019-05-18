from django import forms
from .models import Story, StoryComment


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['url', 'title', 'story_body_text', 'tags']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'story_body_text': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'url': 'آدرس لینک',
            'title': 'عنوان',
            'story_body_text': 'Story body (Use Markdown)',
            'tags': 'تگ'
        }


class StoryCommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ['story_comment']
        widgets = {
            'story_comment': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'story_comment': 'دیدگاه شما چیست'
        }


class RegisterUserForm(forms.Form):
    username = forms.CharField(help_text='نام کاربری دلخواه', strip=True,
                               label='نام کاربری', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=6,
                               label='کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    re_password = forms.CharField(min_length=6, label='تکرار کلمه عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
