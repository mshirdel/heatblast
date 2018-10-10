from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import Story, StoryComment, StoryPoint
from .forms import StoryForm, StoryCommentForm


class Stories(View):
    def get(self, request):
        return render(request, 'socialnews/index.html', {'stories': Story.objects.order_by('-created')})


class ShowStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        story_comment_form = StoryCommentForm()
        return render(request, 'socialnews/show_story.html', {'story': story, 'form': story_comment_form})

    def post(self, request, id):
        story = Story.objects.get(pk=id)
        form = StoryCommentForm(request.POST)
        if form.is_valid():
            comment = StoryComment(commenter=request.user, story=story,
                                   story_comment=form.cleaned_data['story_comment'])
            comment.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/show_story.html', {'story': story, 'form': form})


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
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(instance=story)
        return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})

    def post(self, request, id):
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})


def upvote_story(request, id):
    story = get_object_or_404(Story, pk=id)
    story_point = get_object_or_404(StoryPoint, user=request.user, story=story)
    if (story_point):
        return HttpResponseRedirect('/')
    story_point = StoryPoint(user=request.user, story=story)
    story_point.save()
    return HttpResponseRedirect('/')


def downvote_stroy(request, id):
    story = get_object_or_404(Story, pk=id)
    story_point = get_object_or_404(StoryPoint, story=story, user=request.user)
    if story_point:
        story_point.delete()
    else:
        return HttpResponseRedirect('/')


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'socialnews/profile.html')
