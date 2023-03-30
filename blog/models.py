# blog/models.py
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    likes = models.ManyToManyField(
        "auth.User",
        related_name="likes",
    )

    dislikes = models.ManyToManyField(
        "auth.User",
        related_name="dislikes",
    )
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def rate(self):
        return self.likes.count() - self.dislikes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.ForeignKey(

        "auth.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("post_list")


