from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name = 'user-login'),
    path('register/', views.register_user, name = 'user-register'),
    path('home/profile/', views.profile, name = 'user-profile'),
]