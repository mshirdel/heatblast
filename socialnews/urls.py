from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Stories, PanelView


urlpatterns = [
    path('accounts/login',
         auth_views.LoginView.as_view(template_name='socialnews/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', Stories.as_view(), name='index'),
    path('panel/', PanelView.as_view(), name='admin')
]
