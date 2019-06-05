from django import forms
from django.contrib.auth.models import User
from django_jalali import forms as jforms

from .models import Profile, Story, StoryComment


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


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reapet password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


class SearchForm(forms.Form):
    q = forms.CharField()


class EditUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('photo', 'date_of_birth',)
        widgets = {
            'date_of_birth': jforms.widgets.jDateInput(
                attrs={'class': 'form-control datepicker'}
            )
        }
