from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.


class InstaPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    caption = models.TextField()
    post_img = models.ImageField(upload_to="post_image/")
    created_at = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(InstaPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'


