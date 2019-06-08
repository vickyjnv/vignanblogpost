from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import (
	GroupListView,
	GroupCreateView,
	UserListView,
)
from . import views as views


urlpatterns = [
	path('groups/',GroupListView.as_view() , name = 'groups'),
	path('group/new/', GroupCreateView.as_view(), name='group-create'),
]