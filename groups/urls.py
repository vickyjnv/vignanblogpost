from django.urls import path
from .views import (
	GroupListView,
	GroupCreateView,
)


urlpatterns = [
	path('groups/',GroupListView.as_view() , name = 'groups'),
	path('group/new/', GroupCreateView.as_view(), name='group-create'),
]
