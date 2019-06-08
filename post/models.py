from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from groups.models import Com 
# Create your models here.


class Posts(models.Model):
	title = models.CharField(max_length = 100)
	context = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	groups = models.ForeignKey(Com, on_delete = models.CASCADE)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

