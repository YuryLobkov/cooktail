from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import os
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):

    def image_upload_to(self, instance = None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None

    email = models.EmailField(unique=True)
    image = models.ImageField(default='default/avatardefault_92824.png', upload_to=image_upload_to)
    
    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        return reverse('forum:post-detail', kwargs={'pk': self.pk})

    @property
    def num_of_comments(self):
        return Comment.objects.filter(post=self).count()

    def __str__(self):
        return self.title + '\n' + self.content + (str(self.author))

class Comment(models.Model):
    comment_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('forum:post-detail', kwargs={'pk': self.pk})

