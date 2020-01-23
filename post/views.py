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
from django.db.models import Q
from django.contrib import messages
from .forms import UserRegisterForm, EditProfileForm, EditBasicProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
	posts = Posts.objects.all().order_by('-date_posted')
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	return render(request,'post/index.html', {'posts': posts})
	

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('index')
	else:
		form = UserRegisterForm()
	return render(request, 'post/register.html', {'form': form })

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'post/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = EditProfileForm(instance=request.user.userprofile)
        args = {'form': form}
        return render(request, 'post/update_profile.html', args)

def edit_basic_profile(request):
    if request.method == 'POST':
        form = EditBasicProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = EditBasicProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'post/edit_profile.html', args)



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
	fields = ['title', 'context','image']
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

def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(title__icontains=query) | Q(context__icontains=query)
            results= Posts.objects.filter(lookups).distinct()
            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'post/search.html', context)

        else:
            return render(request, 'post/search.html')

    else:
        return render(request, 'post/search.html')


