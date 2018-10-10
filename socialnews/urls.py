from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Stories, PanelView, NewStory, EditStory, ProfileView, ShowStory, upvote_story


urlpatterns = [
    path('accounts/login',
         auth_views.LoginView.as_view(template_name='socialnews/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('', Stories.as_view(), name='index'),
    path('story/<int:id>', ShowStory.as_view(), name='show_story'),
    path('story/<int:id>/upvote', upvote_story, name='upvote_story'),
    path('story/new', NewStory.as_view(), name='new_story'),
    path('story/<int:id>/edit', EditStory.as_view(), name='edit_story'),
    path('panel/', PanelView.as_view(), name='admin')
]
