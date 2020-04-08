from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ( 'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = UserProfile
        fields = (
            'bio',
            'phone',
            'website',
            'image',
        )

class EditBasicProfileForm(UserChangeForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)