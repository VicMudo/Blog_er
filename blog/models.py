from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class PostQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(content__icontains=query)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    view_count = models.PositiveIntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return f'{self.title}: by {self.author}'

    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.created}'
