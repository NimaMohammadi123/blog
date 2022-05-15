
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from django_quill.fields import QuillField
# Create your models here.


#post

class Post(models.Model):
    
    STATUS =(
        ("draft",'Draft'),
        ("published",'Published')
    )
    
    title =models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25 , choices=STATUS , default="draft")
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="blog_posts")
    slug = models.SlugField(max_length=250 , unique_for_date="publish")
    publish = models.DateTimeField(default = timezone.now)
    tags = TaggableManager()
    content = QuillField(null=True,blank=True)
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    


#comment

class comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comment")
    name = models.CharField(_("نام"),max_length=50)
    body = models.TextField()
    email = models.EmailField(max_length=250 ,null=True,blank=True)
    created =models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)
    active =models.BooleanField(default=True)
    
    class Meta:
        ordering =('created',)
        
    def __str__(self):
        return f'comment by{self.name} on {self.post}'

class QuillPost(models.Model):
    content = QuillField()