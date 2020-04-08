from django.contrib import admin
from .models import Posts, UserProfile, Comment
# Register your models here.

admin.site.register(Posts)

admin.site.register(UserProfile)

admin.site.register(Comment)
