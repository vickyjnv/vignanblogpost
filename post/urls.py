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
from django.conf.urls.static import static


urlpatterns = [
	path('', views.index, name='index'),
	path('profile/', views.view_profile, name='view_profile'),
	path('profile/edit/', views.edit_profile, name='edit_profile'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='post/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='post/logout.html'), name='logout'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('user/<str:username>', UserListView.as_view(), name = 'user-posts'),
	path('groups/<str:name>', GListView.as_view(), name = 'group-posts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)