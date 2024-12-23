from unittest.mock import patch

from django.test import tag
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from posts.models import Post, Comment



class PostTestCase(APITestCase):

    def test_posts_list(self):
        ...