# blog/urls.py
from django.urls import path, include
from django.contrib import admin
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView, # new
    BlogDeleteView,
    LikeView,
    DislikeView,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")), # new
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"), # new
    path("post/<int:pk>/like/", LikeView, name="post_like"), # new
    path("post/<int:pk>/dislike/", DislikeView, name="post_dislike"), # new
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"), # new

    path("", BlogListView.as_view(), name="home"),
]

