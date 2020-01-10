from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Posts
from groups.models import Com 
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def index(request):
	context = {
		'posts' : Posts.objects.all()
	}
	return render(request, "post/index.html", context)


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'post/register.html', {'form': form })


class PostListView(ListView):
	model = Posts
	template_name = 'post/index.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

class UserListView(ListView):
	model = Posts
	template_name = 'post/user_posts.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Posts.objects.filter(user=user).order_by('-date_posted')

class GListView(ListView):
	model = Posts
	template_name = 'post/user_posts.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

	def get_queryset(self):
		name = get_object_or_404(Com, name=self.kwargs.get('name'))
		return Posts.objects.filter(groups=name).order_by('-date_posted')



class PostDetailView(DetailView):
	model = Posts
	


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Posts
	fields = ['groups','title', 'context','image']
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Posts
	fields = ['title', 'context']
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.user:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Posts
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.user:
			return True
		return False

