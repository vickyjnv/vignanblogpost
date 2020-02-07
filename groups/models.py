from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Com(models.Model):
	name = models.CharField(max_length = 100, primary_key=True)
	discripton = models.TextField(default="Test")
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('groups')
	