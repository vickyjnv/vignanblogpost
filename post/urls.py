from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserListView,
	GListView
)
from . import views as views


urlpatterns = [
	path('', PostListView.as_view(), name = 'index'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='post/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='post/logout.html'), name='logout'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('user/<str:username>', UserListView.as_view(), name = 'user-posts'),
	path('groups/<str:name>', GListView.as_view(), name = 'group-posts'),
]