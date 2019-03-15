from django.contrib import admin
from .models import Post, Subscription


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    model = Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'author', 'title', 'text', 'created']
    readonly_fields = ['created', 'updated']
    filter_horizontal = ['seen_by']

