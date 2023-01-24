from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone 

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    post_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('forum:post-detail', kwargs={'pk': self.pk})
