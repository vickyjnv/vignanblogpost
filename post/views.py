from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Posts
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from groups.models import Com
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import login ,get_user_model
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage , send_mail
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	FormView,
)
from django.contrib.auth.decorators import login_required
from django import forms
from django.template import loader
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from .forms import UserRegisterForm, EditProfileForm, EditBasicProfileForm, CommentForm ,PasswordResetRequestForm
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def index(request):
	posts = Posts.objects.all().order_by('-date_posted')
	groups = Com.objects.all()
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	return render(request,'post/index.html', {'posts': posts , 'groups':groups})

@login_required
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
			# user.is_active = False
			user.save()
			# current_site = get_current_site(request)
			# mail_subject = 'Activate your blog account.'
			# message = render_to_string('acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activation_token.make_token(user),
            # })
			# to_email = form.cleaned_data.get('email')
			# email = EmailMessage(mail_subject, message, to=[to_email])
			# email.send()
			# username = form.cleaned_data.get('username')
			# messages.success(request, f'Account created for {username}!')
			# messages.info(request, f'Please confirm your email address to complete the registration')
			# return render(request,'email.html', {'to_email': to_email})
			return redirect('index')
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

@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'post/profile.html', args)

@login_required
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

@login_required
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


DEFAULT_FROM_EMAIL = "saibaaskar24091999@gmail.com"
class ResetPasswordRequestView(FormView):
    template_name = "test_template.html"
    success_url = '/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'VIIT Blog',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='password_reset_subject.txt'
                        email_template_name='password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'VIIT Blog',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='password_reset_subject.txt'
                    email_template_name='password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)

class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class PasswordResetConfirmView(FormView):
    template_name = "test_template.html"
    success_url = '/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)

