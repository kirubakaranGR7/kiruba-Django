from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    OPTION = (
        ('draft','Draft'),
        ('published','Public')
    )

    tittle = models.CharField(max_length=100,default=None)
    slug = models.SlugField(max_length=100,unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_post')
    content = models.TextField()
    status = models.CharField(max_length=100,choices=OPTION,default='draft')

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.tittle



