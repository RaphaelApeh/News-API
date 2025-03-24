from django.test import TestCase
from django.utils.lorem_ipsum import WORDS
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from posts.models import Post

User = get_user_model()


class PostTestCase(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user("testuser", "testpassword")
        Post.objects.create(
            user=user, title="A good article post", content=" ".join(WORDS)
        )

    def test_post_create(self):

        user = User.objects.create_user("admin", "testpassword")
        Post.objects.create(
            user=user, title="A terrible title", content=" ".join(WORDS)
        )

    def test_invalid_post_create(self):

        user = User.objects.create_user("admin", "testpassword")
        post = Post.objects.create(user=user, content=" ".join(WORDS))  # No title

        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_reverse_comment_create(self):

        post = Post.objects.first()
        post.posts.create(user=post.user, content="A good article")

        self.assertTrue(post.posts.exists())
