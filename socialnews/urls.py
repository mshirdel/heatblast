from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (PanelView, NewStory, EditStory, ProfileView, ShowStory,
                    upvote_story, downvote_stroy, RegisterUserView,
                    StoryListView, fetch_title, test)

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
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/register/', RegisterUserView.as_view(), name='register_user'),

    ###################
    # STORIES         #
    ###################

    path('', StoryListView.as_view(), name='index'),
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
    path('test/', test),
]
