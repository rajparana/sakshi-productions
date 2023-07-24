from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField


status = [("Active", "Active"), ("Hidden", "Hidden"), ("Inactive", "Inactive"), ("Delete", "Delete")]


class User(AbstractUser):
    email = models.EmailField(max_length=160, unique=True)
    mobile = models.CharField(max_length=180, null=True, unique=True)
    image = models.ImageField(upload_to='profile/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')

    unique_together = ['email', 'username']

    def save(self, *args, **kwargs):
        self.username = self.email
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "01. Users"


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "02. Categories"


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
    status = models.CharField(max_length=20, choices=status, default='Active')
    
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

    class Meta:
        verbose_name_plural = "03. Posts"


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
    status = models.CharField(max_length=20, choices=status, default='Active')
    
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

    class Meta:
        verbose_name_plural = "04. Album"


class TopQuote(models.Model):
    image = models.ImageField(upload_to='top-quote/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def top_quote_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""
    
    class Meta:
        verbose_name_plural = "05. Top Quote (Home)"


class BottomQuote(models.Model):
    image = models.ImageField(upload_to='bottom-quote/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def bottom_quote_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "06. Bottom Quote (Home)"


class CollageCrousel(models.Model):
    image = models.ImageField(upload_to='collage-crousel/', blank=True, null=True)
    feature = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image.url

    @property
    def collage_crousel_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "07. Collage Crousel (Home)"


class SlideCrousel(models.Model):
    image = models.ImageField(upload_to='slide-crousel/', blank=True, null=True)
    feature = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image.url

    @property
    def slide_crousel_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "08. Slide Crousel (Home)"


class Reach(models.Model):
    image = models.ImageField(upload_to='reach/', blank=True, null=True)
    text = RichTextField()
    button = models.CharField(max_length=40, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def reach_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "09. Reach Us (Home)"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, null=True, blank=False)
    comment = models.TextField()
    image = models.ImageField(upload_to='client/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def client_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "10. Testimonials (Home)"


class TopAbout(models.Model):
    image = models.ImageField(upload_to='top-about/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def top_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "11. Top (About)"


class MidAbout(models.Model):
    image = models.ImageField(upload_to='mid-about/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def mid_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "12. Mid (About)"


class BottomAbout(models.Model):
    image = models.ImageField(upload_to='bottom-about/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def bottom_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "13. Bottom (About)"


class AboutQuote(models.Model):
    image = models.ImageField(upload_to='about-quote/', blank=True, null=True)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]

    @property
    def bottom_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "14. Quote (About)"


class Service(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    icon = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "15. Services (About)"


class Expertise(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='expertise/', blank=True, null=True)
    instagram = models.CharField(max_length=280, null=True, blank=True)
    facebook = models.CharField(max_length=280, null=True, blank=True)
    twitter = models.CharField(max_length=280, null=True, blank=True)
    linkedin = models.CharField(max_length=280, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def bottom_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "16. Expertise (About)"


class Contact(models.Model):
    email = models.EmailField()
    call = models.CharField(max_length=25)
    image = models.ImageField(upload_to='contact/', blank=True, null=True)
    address = models.CharField(max_length=280)
    location = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status, default='Active')
    
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def bottom_about_image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" height="80" />'.format(self.image.url))
        return ""

    class Meta:
        verbose_name_plural = "17. Contact Us"
