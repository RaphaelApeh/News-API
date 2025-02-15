from django.test import tag
from django.utils.lorem_ipsum import WORDS
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Post

User = get_user_model()

@tag("posts", "post")
class PostAPITestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user("admin", "testpassword")
        Post.objects.create(user=user, title="A terrible title", content=" ".join(WORDS))
        self.user = user
        return super().setUp()

    def test_posts_list_view(self):
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse("posts-list"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post_detail_view(self):
        
        self.client.force_login(self.user)
        obj = Post.objects.first()
        response = self.client.get(reverse("posts-detail", kwargs={"slug": obj.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_request(self):
        
        self.client.force_login(self.user)
        data = {
            "user": self.user,
            "title": "A Good Title",
            "content": " ".join(WORDS),
            "status": "active"
        }
        response = self.client.post(reverse("posts-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        