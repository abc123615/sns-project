from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('following/', views.following_posts, name='following_posts'),
    path('posts/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('posts/new/', views.post_create, name='post_create'),
    path('signup/', views.signup, name='signup'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('users/search/', views.user_search, name='user_search'),
]