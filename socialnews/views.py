from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import Story
from .forms import StoryForm


class Stories(View):
    def get(self, request):
        return render(request, 'socialnews/index.html', {'items': Story.objects.all()})


class ShowStory(View):
    def get(self, request, id):
        story = Story.objects.get(pk=id)
        return render(request, 'socialnews/show_story.html', {'story': story})


class NewStory(View):
    def get(self, request):
        form = StoryForm()
        return render(request, 'socialnews/new_story.html', {'form': form})

    def post(self, request):
        form = StoryForm(request.POST)
        if form.is_valid():
            story = Story(title=form.cleaned_data['title'],
                          url=form.cleaned_data['url'],
                          story_body_text=form.cleaned_data['story_body_text'],
                          user=request.user
                          )
            story.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/new_story.html', {'form': form})


class EditStory(View):
    def get(self, request, id):
        story = Story.objects.get(pk=id)
        form = StoryForm(instance=story)
        return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})

    def post(self, request, id):
        story = Story.objects.get(pk=id)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'socialnews/profile.html')
