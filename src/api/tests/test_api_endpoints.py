from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from posts.models import Post, Comment

User = get_user_model()

TEST_USERNAME = "admin"
TEST_PASSWORD = 'test'

class APIEndPointTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_superuser(username=TEST_USERNAME, password=TEST_PASSWORD)
        obj = {"user":user, "title":"Test post", "text":"A body text."}
        self.post = Post.objects.create(**obj)

    def test_post_exists(self):
        post = Post.objects.all()
        self.assertTrue(post.exists())

    def test_list_posts(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get(reverse('list-posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_post_view(self):
        
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get(reverse('post-detail', kwargs={'slug': self.post.slug}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_view(self):
        ...