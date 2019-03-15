import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from blog.models import Post, Subscription, User
from api.serializers import UserSerializer, PostSerializer


class PostsAPIViewTestCase(APITestCase):

    def setUp(self):
        self.items_on_page = 10
        self.username = "john"
        self.email = "john_doe@mail.com"
        self.password = "password"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.post = Post.objects.create(author=self.user, title="Test post title!", text="Test post text!")
        self.url = reverse("posts_list_api")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_object_create(self):
        """
            Test to verify post object creation
        """
        response = self.client.post(self.url, {"title": self.post.title,
                                               "text": self.post.text})
        self.assertEqual(201, response.status_code)
        response_data = json.loads(response.content)
        self.assertEqual(self.post.title, response_data['title'])
        self.assertEqual(self.post.text, response_data['text'])

    def test_post_object_get_list(self):
        """
            Test to verify post objects data
        """
        response = self.client.get(self.url)
        response_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Post.objects.all().count(), response_data['count'])
        self.assertGreaterEqual(self.items_on_page, len(response_data['results']))

    def test_post_objects_sorting(self):
        """
            Test to verify correctly post ordering
        """
        Post.objects.create(author=self.user, title="2", text="second").save()
        Post.objects.create(author=self.user, title="3", text="third").save()
        response = self.client.get(self.url)
        response_data = json.loads(response.content)
        self.assertGreaterEqual(response_data['results'][0]['created'], response_data['results'][-1]['created'])

