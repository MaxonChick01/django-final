# articles/admin.py
from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline): # new
    model = Comment

class PostAdmin(admin.ModelAdmin): # new
    inlines = [
        CommentInline,
    ]
admin.site.register(Post, PostAdmin) # new
admin.site.register(Comment)