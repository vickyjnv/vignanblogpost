from django.shortcuts import render
from .models import Com
from post.models import Posts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
# Create your views here.

def group(request):
	context = {
		'group' : Com.objects.all()
	}
	return render(request, "groups/groups.html", context)


class GroupListView(ListView):
	model = Com
	template_name = 'groups/groups.html'
	context_object_name = 'group'
	ordering = ['-name']



class GroupCreateView(LoginRequiredMixin, CreateView):
	model = Com
	fields = ['name']


class UserListView(ListView):
	model = Posts
	template_name = 'groups/group_posts.html'
	context_object_name = 'group'
	ordering = ['-date_posted']

	def get_queryset(self):
		user = get_object_or_404(User, name=self.kwargs.get('name'))
		return Posts.objects.filter(user=user).order_by('-date_posted')