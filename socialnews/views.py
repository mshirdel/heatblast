import requests
import uuid
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission, User
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import ListView
from taggit.models import Tag

from .forms import (EditProfileForm, EditUserForm, RegisterUserForm,
                    SearchForm, StoryCommentForm, StoryForm)
from .models import Profile, Story, StoryComment, StoryPoint


class StoryListView(ListView):
    queryset = Story.stories.all().order_by('-number_of_votes')
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
        if self.request.path == '/story/latest/':
            return Story.stories.all().order_by('-created')
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
                return render(request, 'socialnews/story/show.html',
                              {'story': story, 'form': StoryCommentForm})
            else:
                return render(request, 'socialnews/story/show.html',
                              {'story': story, 'form': form})
        else:
            form = StoryCommentForm()
            messages.add_message(request,
                                 messages.WARNING,
                                 _('Please Register to site for commenting')
                                 )
            return render(request, 'socialnews/story/show.html',
                          {'story': story, 'form': form})


@method_decorator(login_required, name='dispatch')
class NewStory(PermissionRequiredMixin, View):
    permission_required = 'socialnews.add_story'

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
        return render(request, 'socialnews/profile/profile.html')


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request):
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'socialnews/profile/edit.html', context)

    def post(self, request):
        user_form = EditUserForm(instance=request.user, data=request.POST)
        profile_form = EditProfileForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated")
        else:
            messages.error(request, "Somthing goes wrong")
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'socialnews/profile/edit.html', context)


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'socialnews/register_user.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.send_activation_code(request)
            messages.success(request, _('Successfully created your account. for activating it check your email'))
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/register_user.html', {'form': form})


def email_confirmation(request, token, code):
    user_token = uuid.UUID(token)
    user = get_object_or_404(User, profile__token=user_token)
    if user.is_active:
        messages.info(request, _('Your account already activated'))
        return HttpResponseRedirect('/')
    if str(user.profile.activation_code) == code:
        user.is_active = True
        user.save()
        messages.success(request, _("Your account is active. You can login now."))
        return HttpResponseRedirect('/')
    return render(request, 'socialnews/profile/activation_email_done.html',
                  {'activation_status': user.is_active})


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


class Test(View):
    def get(self, request):
        return render(request, 'socialnews/test.html')

    def post(self, request):
        messages.success(request, 'everything is OK')
        return render(request, 'socialnews/test.html')
