from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    tags = TaggableManager()
    image = models.ImageField(upload_to='post_images')
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, **kwargs):
        if self.slug is not None:
            self.slug = slugify(self.title)
        super().save(**kwargs)

    def comments(self):
        
        return self.comment_set.all()
    
    def get_user_display_name(self):

        return self.user.get_full_name() or self.user.username

class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title