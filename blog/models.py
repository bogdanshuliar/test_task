from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=False, null=True)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seen_by = models.ManyToManyField(User, related_name='seen_by_users', blank=True)

    class Meta(object):
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return 'Post #' + str(self.id)


class Subscription(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_provider')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscriber')
    subscribe_date = models.DateTimeField(auto_now_add=True)
