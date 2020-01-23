from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from groups.models import Com 
from django.db.models.signals import post_save
# Create your models here.


class Posts(models.Model):
	title = models.CharField(max_length = 100)
	context = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	groups = models.ForeignKey(Com, on_delete = models.CASCADE)
	image = models.ImageField(upload_to='post_images', blank=True)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
	def __str__(self):
		return self.title



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length=100, default='',blank = True)
    website = models.URLField(default='',blank = True)
    phone = models.IntegerField(default=0,blank = True)
    image = models.ImageField(upload_to='profile_image',default = 'octocat.png')

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        post_save.connect(create_profile, sender=User)