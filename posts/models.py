from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.text import Truncator, slugify

User = getattr(settings, "AUTH_USER_MODEL")

class StatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    PENDING = "pending", "Pending"
    DRAFT = "draft", "Draft"

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.user_id}"
    
    def save(self, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)[:10]
        super().save(**kwargs)

    @property
    def short_content(self):
        return Truncator(self.content).words(50)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]