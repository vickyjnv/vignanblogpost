from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from groups.models import Com
from django.db.models.signals import post_save
from imagekit.models.fields import ProcessedImageField , ImageSpecField
from imagekit.processors import ResizeToFill

User._meta.get_field('email')._unique = True

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


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length=100, default='',blank = True)
    website = models.URLField(default='',blank = True)
    phone = models.CharField( max_length=15, blank=True) # validators should be a list
    #image = models.ImageField(upload_to='profile_image',default = 'octocat.png')
    image = ProcessedImageField(default="octocat.png", upload_to='profile_image',processors=[ResizeToFill(200,200)], format='JPEG', options={'quality': 90})
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(50, 50)],format='JPEG',options={'quality': 100})

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)