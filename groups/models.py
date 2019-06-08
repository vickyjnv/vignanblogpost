from django.db import models
from django.urls import reverse
# Create your models here.

class Com(models.Model):
	name = models.CharField(max_length = 100, primary_key=True)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('groups')
	