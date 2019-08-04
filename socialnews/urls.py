from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from socialnews.sitemaps import StorySitemap

from .feeds import LatesStoryFeed
from .views import (EditStory, NewStory, PanelView, ProfileView,
                    RegisterUserView, ShowStory, StoryListView, downvote_stroy,
                    fetch_title, story_search, upvote_story,
                    ProfileEditView, email_confirmation,
                    Test)

sitemaps = {
    'stories': StorySitemap
}

app_name = 'socialnews'
urlpatterns = [
    ###################
    # AUTH            #
    ###################

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='socialnews/login.html'),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'),
         name='logout'),

    path('accounts/register/', RegisterUserView.as_view(), name='register_user'),
    path('accounts/password_change', auth_views.PasswordChangeView.as_view(
        success_url='/accounts/password_change_done'), name='password_change'),
    path('accounts/password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(success_url='/accounts/password_reset_done'), name='password_reset'),
    path('accounts/password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/accounts/reset/done'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('accounts/email_confirmation/<token>/<code>',
         email_confirmation, name='email_confitmation'),

    ###################
    # PROFILE         #
    ###################

    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),

    ###################
    # STORIES         #
    ###################

    path('', StoryListView.as_view(), name='index'),
    path('story/tag/<slug:tag_slug>',
         StoryListView.as_view(), name='story_list_by_tag'),
    path('story/latest/', StoryListView.as_view(), name='latest_stories'),
    path('story/<int:id>', ShowStory.as_view(), name='show_story'),
    path('story/upvote/<int:id>', upvote_story, name='upvote_story'),
    path('story/downvote/<int:id>', downvote_stroy, name='downvote_story'),
    path('story/new', NewStory.as_view(), name='new_story'),
    path('story/edit/<int:id>', EditStory.as_view(), name='edit_story'),
    path('story/site', StoryListView.as_view(), name='stories_by_domain'),
    path('story/fetch_title', fetch_title, name='fetch_title'),

    ###################
    # OTHER           #
    ###################

    path('panel/', PanelView.as_view(), name='admin'),
    path('test/', Test.as_view()),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.view.sitemap'),
    path('feed/', LatesStoryFeed(), name='story_feed'),
    path('search/', story_search, name='story_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
