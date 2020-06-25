from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'blog-home'),
    path('myPost/', views.myPost, name = 'blog-myPost'),
    path('addPost/', views.PostCreateView.as_view(), name = 'blog-addPost'),
    path('myPost/<pk>/update/', views.post_update, name='post-update'),
    path('myPost/<pk>/delete/', views.post_delete, name='post-delete'),
    path('logout/', views.logout_user, name = 'logout-user'),
    path('<author>Profile/', views.authorProfile, name = 'blog-authorProfile')
]