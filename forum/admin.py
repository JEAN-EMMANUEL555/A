from django.contrib import admin
from .models import UserProfile, Post, Comment, Like

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
