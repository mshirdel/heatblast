from django import forms
from django.contrib.auth.models import User
from django_jalali import forms as jforms
from django.utils.translation import gettext_lazy as _

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


class StoryCommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ['story_comment']
        widgets = {
            'story_comment': forms.Textarea(attrs={'class': 'form-control'})
        }


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Reapet password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if email and User.objects.get(email=email):
                raise forms.ValidationError('Email address must be unique')
        except User.DoesNotExist:
            return email


class SearchForm(forms.Form):
    q = forms.CharField()


class EditUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address must be unique')
        else:
            return email


class EditProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('photo', 'date_of_birth',)
        widgets = {
            'date_of_birth': jforms.widgets.jDateInput(
                attrs={'class': 'form-control datepicker'}
            )
        }
