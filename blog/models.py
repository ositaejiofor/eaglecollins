from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import Truncator




# Create your models here.

STATUS = (
    ( 0, 'Draft'),
    (1, 'Publish')
)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    # ... other fields

    @property
    def excerpt(self):
        return Truncator(self.body).words(25, truncate='...')


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags
    summary = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    published_date = models.DateField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='technologies/', blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    blog_id = models.IntegerField(blank=True, null=True)  
    # Add this field to store the Blog ID
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    def save(self, *args, **kwargs):
        # Automatically set the blog_id when saving a comment
        if self.post:
            self.blog_id = self.post.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

def get_absolute_url(self):
    return reverse('blog_detail', args=[str(self.id)])


    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

# inside Blog model
def get_absolute_url(self):
    return reverse('blog_detail', args=[str(self.id)])
