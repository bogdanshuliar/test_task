from django.urls import path
from api.views import (UsersListApiView, PostsListApiView, SubscriptionApiView, PostDetailApiView)

urlpatterns = [
    # Auth URLs
    path("posts/", PostsListApiView.as_view(), name="posts_list_api"),
    path("users/", UsersListApiView.as_view(), name="users_list_api"),
    path("users/<int:pk>/subscribe/", SubscriptionApiView.as_view(), name="subscription_api"),
    path("posts/<int:pk>/", PostDetailApiView.as_view(), name="posts_detail_view"),
]
