import requests
from bs4 import BeautifulSoup

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag

from .models import Story, StoryComment, StoryPoint
from .forms import StoryForm, StoryCommentForm, RegisterUserForm, SearchForm


class StoryListView(ListView):
    queryset = Story.objects.all()
    context_object_name = 'stories'
    paginate_by = settings.PAGE_SIZE
    template_name = 'socialnews/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voted_story_id = []
        if self.request.user.is_authenticated:
            for point in self.request.user.storypoint_set.all():
                voted_story_id.append(point.story_id)
        context['voted_story_id'] = voted_story_id
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.GET.get('url'):
            url = self.request.GET.get('url')
            return query_set.filter(url_domain_name=url)
        if self.kwargs.get('tag_slug'):
            tag_slug = self.kwargs.get('tag_slug')
            tag = get_object_or_404(Tag, slug=tag_slug)
            messages.add_message(self.request,
                                 messages.INFO,
                                 f"Stories tagged with {tag_slug}")
            return query_set.filter(tags__in=[tag])
        return query_set


class ShowStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        story_tags_ids = story.tags.values_list('id', flat=True)
        similar_stories = Story.stories.filter(
            tags__in=story_tags_ids).exclude(id=story.id)
        similar_stories = similar_stories.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        story_comment_form = StoryCommentForm()
        return render(request, 'socialnews/story/show.html',
                      {
                          'story': story,
                          'form': story_comment_form,
                          'similar_stories': similar_stories
                      })

    def post(self, request, id):
        story = get_object_or_404(Story, pk=id)
        if request.user.is_authenticated:
            form = StoryCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.commenter = request.user
                comment.story = story
                comment.save()
                return HttpResponseRedirect('/')
            else:
                return render(request, 'socialnews/story/show.html',
                              {'story': story, 'form': form})
        else:
            form = StoryCommentForm()
            messages.add_message(request,
                                 messages.WARNING,
                                 "برای ثبت دیدگاه باید دارای حساب کاربری باشید.")
            return render(request, 'socialnews/story/show.html',
                          {'story': story, 'form': form})


@method_decorator(login_required, name='dispatch')
class NewStory(View):
    def get(self, request):
        form = StoryForm()
        return render(request, 'socialnews/story/new.html', {'form': form})

    def post(self, request):
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            form.save_m2m()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/story/new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
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
            story.tags.clear()
            for tag_slug in form.cleaned_data['tags']:
                story.tags.add(tag_slug)
            story.save()
            # form.save_m2m() # produce error => 'StoryForm' object has no attribute 'save_m2m'
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/story/edit.html',
                          {'form': form, 'id': id})


@login_required()
def upvote_story(request, id):
    result_url = '/'
    if request.GET.get('page'):
        result_url = f"/?page={request.GET.get('page')}"
    story = get_object_or_404(Story, pk=id)
    try:
        StoryPoint.objects.get(user=request.user, story=story)
        return HttpResponseRedirect(result_url)
    except StoryPoint.DoesNotExist:
        story_point = StoryPoint(user=request.user, story=story)
        story_point.save()
        return HttpResponseRedirect(result_url)


@login_required()
def downvote_stroy(request, id):
    result_url = '/'
    if request.GET.get('page'):
        result_url = f"/?page={request.GET.get('page')}"
    try:
        story_point = StoryPoint.objects.get(user=request.user, story_id=id)
        story_point.delete()
    except StoryPoint.DoesNotExist:
        pass
    return HttpResponseRedirect(result_url)


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')


@method_decorator(login_required, name='dispatch')
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


def fetch_title(request):
    url = request.GET.get('url', None)
    if url is not None:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return JsonResponse({'title': soup.title.text})
        else:
            return JsonResponse({'error': 'fetch title not work'})
    else:
        return JsonResponse({'error': 'url not found'})


def story_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            search_vector = SearchVector('title', 'story_body_text')
            search_query = SearchQuery(query)
            results = Story.stories.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
    context = {'query': query, 'results': results}
    return render(request, 'socialnews/search_result.html', context)


def test(request, id):
    story = get_object_or_404(Story, id=id)
    subject = story.title
    message = request.build_absolute_uri(story.get_absolute_url())
    send_mail(subject, message, 'helermiles@gmail.com', ['mshirdel@gmail.com'])
    return HttpResponse(f"{subject} has been sent")
