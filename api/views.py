from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import PostSerializer, UserSerializer
from django.db.models import Count
from blog.models import Post, User, Subscription
from json import loads


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class UsersListApiView(ListAPIView):
    """
        get:
        Get list of users.
        Order users by count of posts if 'subscriber' is true
        parameters:
        - in: query
          name: offset
          schema:
            type: integer
          description: The number of items to skip before starting to collect the result set
        - in: query
          name: limit
          schema:
            type: integer
          description: The numbers of items to return
    """

    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.filter()
        if loads(self.request.query_params.get('sort', 'false')):
            return queryset.annotate(posts_count=Count('post')).order_by('-posts_count')
        else:
            return queryset


class PostsListApiView(ListCreateAPIView):
    """
       get:
       Get list of post objects.

       post:
       Create new post.
    """

    model = Post
    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        subscriber = loads(self.request.query_params.get('subscriber', 'false'))
        seen = loads(self.request.query_params.get('seen', 'false'))

        if subscriber:
            subscriptions = Subscription.objects.filter(subscriber=self.request.user)
            queryset = Post.objects.none()

            for subscription in subscriptions:
                posts_by_author = Post.objects.filter(author_id=subscription.provider_id,
                                                      created__gt=subscription.subscribe_date)

                if seen:
                    posts_by_author = posts_by_author.exclude(seen_by__in=[self.request.user])

                queryset = queryset.union(posts_by_author)

            return queryset.order_by('-created')
        else:
            return Post.objects.all().order_by('-created')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'user': self.request.user}


class SubscriptionApiView(RetrieveModelMixin, CreateModelMixin, APIView):
    """
       get:
       Get current state of the subscription to a user.

       post:
       Subscribe/unsubscribe to user .
    """

    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        try:
            Subscription.objects.get(provider_id=kwargs['pk'],
                                     subscriber=self.request.user)
            return Response({'subscribed': True}, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response({'subscribed': False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, *args, **kwargs):
        subscription, created = Subscription.objects.get_or_create(provider_id=kwargs['pk'],
                                                                   subscriber=self.request.user)
        if not created:
            subscription.delete()
            return Response('unsubscribed', status=status.HTTP_202_ACCEPTED)
        else:
            subscription.save()
            return Response('subscribed', status=status.HTTP_200_OK)


class PostDetailApiView(CreateModelMixin, APIView):
    """
       post:
       Mark post as seen.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['pk'])
            post.seen_by.add(self.request.user)
            post.save()
            return Response(status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
