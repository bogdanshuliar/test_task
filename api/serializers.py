from rest_framework import serializers
from blog.models import Post, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'created']

    def create(self, validated_data):
        validated_data['author'] = self.context['user']
        post = Post.objects.create(**validated_data)
        post.save()
        return post
