from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField


class User(AbstractUser):
    email = models.EmailField(max_length=160, unique=True)
    mobile = models.CharField(max_length=180, null=True, unique=True)
    image = models.ImageField(upload_to='profile/')

    unique_together = ['email', 'username']

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    text = RichTextField()
    destination = models.CharField(max_length=500, blank=True, null=True)
    youtube = models.CharField(max_length=500, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_image(self):
        return self.thumbnail

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.thumbnail.url))
        return ""


class Album(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='album_category')
    album = models.FileField(upload_to='albums/', blank=True, null=True)
    top_quote = models.BooleanField(default=False)
    bottom_quote = models.BooleanField(default=False)
    crousel = models.BooleanField(default=False)
    testimonial = models.BooleanField(default=False)
    reach_us = models.BooleanField(default=False)
    about_top = models.BooleanField(default=False)
    about_middle = models.BooleanField(default=False)
    about_bottom = models.BooleanField(default=False)
    about_quote = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    head = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_image(self):
        return self.album

    def __str__(self):
        return self.post.title

    @property
    def album_preview(self):
        if self.album:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.album.url))
        return ""
