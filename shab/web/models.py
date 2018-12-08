from django.db import models
from django_jalali.db import models as jmodels
from taggit.managers import TaggableManager
from django.contrib.sessions.models import Session





# Create your models here.
import datetime

class Post(models.Model):
    Title = models.TextField(blank=False)
    Type = models.CharField(max_length=50)
    Category = models.CharField(max_length=50)
    SubTitle = models.TextField(null=True , blank=True)
    About = models.TextField(null=True, blank=True)
    Author = models.CharField(max_length=50 , null=True, blank=True)
    Avatar = models.ImageField(upload_to='static/image/avatar/' , null=True , blank=True)
    Text = models.TextField()
    objects = jmodels.jManager()
    Date = jmodels.jDateField()
    AparatLink = models.TextField(null=True, blank=True)
    PostImage = models.ImageField(upload_to='static/image/post/', null=True , blank=True)
    tags = TaggableManager()


class Comment(models.Model):
    RelPost = models.ForeignKey(Post,on_delete=models.CASCADE)
    Text = models.TextField()
    Author = models.CharField(max_length=50)
    objects = jmodels.jManager()
    Date = jmodels.jDateField()
    models.DateTimeField(default=datetime.datetime.now())
    Email = models.EmailField(null=True)
    Valid = models.BooleanField(default=False)

class Like(models.Model):
    RelPost = models.ForeignKey(Post,on_delete=models.CASCADE)
    User = models.ForeignKey(Session, on_delete=models.SET_NULL , null=True)


class Banner(models.Model) :
    PostLink = models.ForeignKey(Post , related_name='banner' ,  on_delete=models.CASCADE)