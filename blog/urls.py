from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('home/', views.PostListView.as_view(), name="blog_home"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('post/new/', views.PostCreateView.as_view(), name="post_new"),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),
    path('user/<str:username>/', views.UserPostListView.as_view(), name="user_posts"),
    path('handle_email/', views.handle_feedback_email, name="handle_email"),
   # path('search/', views.search, name="search"),
    
]