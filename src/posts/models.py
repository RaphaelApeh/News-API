from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from rest_framework.reverse import reverse


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    text = models.TextField()
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    image = models.ImageField(upload_to='post_images', default='default.jpg')
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(**kwargs)

    def comments(self):
        
        return self.comment_set.all()
    
    def get_user_display_name(self)-> str:

        return self.user.get_full_name() or self.user.username
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    def get_comments_url(self):
        return
    
    def likes_count(self)-> int:
        return self.likes.count()
    
    def image_url(self)-> str:
        return settings.URL + self.image.url
    
    def get_timestamp_format(self):
        return self.timestamp.strftime("%d/%m/%Y, %H:%M:%S")


class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self)-> str:
        return self.post.title