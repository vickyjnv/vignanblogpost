from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Posts
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from groups.models import Com
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .forms import UserRegisterForm, EditProfileForm, EditBasicProfileForm, CommentForm
from django.core.paginator import Paginator


def index(request):
	posts = Posts.objects.all().order_by('-date_posted')
	groups = Com.objects.all()
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	return render(request,'post/index.html', {'posts': posts , 'groups':groups})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Posts, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'post/add_comment_to_post.html', {'form': form})


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			messages.info(request, f'Please confirm your email address to complete the registration')
			return render(request,'email.html', {'to_email': to_email})
	else:
		form = UserRegisterForm()
	return render(request, 'post/register.html', {'form': form })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account. {user}!')
    else:
        messages.success(request, f'Activation link is invalid!')
    return redirect('index')

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
	model = Posts, Com
	template_name = 'groups/group_posts.html'
	context_object_name = 'posts'

	def get_context_data(self, **kwargs):
		name = get_object_or_404(Com, name=self.kwargs.get('name'))
		context = super(GListView, self).get_context_data(**kwargs)
		context['groups'] = Com.objects.filter(name = name)
		return context

	def get_queryset(self):
		name = get_object_or_404(Com, name=self.kwargs.get('name'))
		return Posts.objects.filter(groups=name).order_by('-date_posted')



class PostDetailView(DetailView):
	model = Posts


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Posts
	fields = ['groups','title', 'context','image']
	def form_valid(self, form):
		title = form.cleaned_data.get('title')
		group = form.cleaned_data.get('groups')
		obj = Com.objects.filter(name=group)
		val = obj.first().count
		val+=1
		obj.update(count=val)
		messages.success(self.request, f'Post with title {title} Created!')
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


