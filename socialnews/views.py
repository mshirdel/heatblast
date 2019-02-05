from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Story, StoryComment, StoryPoint
from .forms import StoryForm, StoryCommentForm, RegisterUserForm


class Stories(View):
    def get(self, request):
        voted_story_id = []
        all_stories = Story.objects.all()
        paginator = Paginator(all_stories, settings.PAGE_SIZE)
        page = request.GET.get('page')
        try:
            stories = paginator.page(page)
        except PageNotAnInteger:
            stories = paginator.page(1)
        except EmptyPage:
            stories = paginator.page(paginator.num_pages)
        if request.user.is_authenticated:
            for point in request.user.storypoint_set.all():
                voted_story_id.append(point.story_id)
        return render(request, 'socialnews/index.html', {
            'stories': stories,
            'voted_story_id': voted_story_id,
            'page': page,
            'num_pages': list(range(paginator.num_pages))
        })


class ShowStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        story_comment_form = StoryCommentForm()
        return render(request, 'socialnews/story/show.html',
                      {'story': story, 'form': story_comment_form})

    def post(self, request, id):
        story = Story.objects.get(pk=id)
        form = StoryCommentForm(request.POST)
        if form.is_valid():
            comment = StoryComment(commenter=request.user, story=story,
                                   story_comment=form.cleaned_data['story_comment'])
            comment.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/story/show.html',
                          {'story': story, 'form': form})


class NewStory(View):
    def get(self, request):
        form = StoryForm()
        return render(request, 'socialnews/story/new.html', {'form': form})

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
            return render(request, 'socialnews/story/new.html', {'form': form})


class EditStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(instance=story)
        return render(request, 'socialnews/story/edit.html',
                      {'form': form, 'id': id})

    def post(self, request, id):
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/story/edit.html',
                          {'form': form, 'id': id})


@login_required()
def upvote_story(request, id):
    story = get_object_or_404(Story, pk=id)
    try:
        story_point = StoryPoint.objects.get(user=request.user, story=story)
        return HttpResponseRedirect('/')
    except StoryPoint.DoesNotExist:
        story_point = StoryPoint(user=request.user, story=story)
        story_point.save()
        return HttpResponseRedirect('/')


@login_required()
def downvote_stroy(request, id):
    try:
        story_point = StoryPoint.objects.get(user=request.user, story_id=id)
        story_point.delete()
    except StoryPoint.DoesNotExist:
        pass
    return HttpResponseRedirect('/')


def filter_story_by_domain(request):
    url = request.GET.get('url')
    filtered_stories = Story.objects.filter(url_domain_name=url)
    paginator = Paginator(filtered_stories, settings.PAGE_SIZE)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)
    return render(request, 'socialnews/index.html', {
        'stories': stories,
        'page': page,
        'num_pages': list(range(paginator.num_pages))
    })


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'socialnews/profile.html')


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'socialnews/register_user.html', {'form': form})

    def post(self, request):
        errors = []
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['re_password']:
                if get_object_or_404(User, username=form.cleaned_data['username']):
                    errors.append('این نام کاربری قبلا استفاده شده است.')
                    return render(request, 'socialnews/register_user.html', {'form': form, 'errors': errors})
                else:
                    new_user = User.objects.create_user(
                        form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
                    new_user.save()
            else:
                errors.append('کلمه عبور و تکرار کلمه با هم برابر نیست.')
                return render(request, 'socialnews/register_user.html', {'form': form, 'errors': errors})
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/register_user.html', {'form': form, 'errors': form.errors})
