from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    # articles (implicit)
    name = models.CharField(max_length = 200)
    url = models.URLField() 
    user = models.ForeignKey(User)
    notes = models.TextField()

    def __unicode__(self):
        return self.name

class Article(models.Model):
    url = models.URLField()
    author = models.ForeignKey(Author, null=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    read_date = models.DateTimeField('date read')
    vote = models.IntegerField()
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("url","user")
    
    def __unicode(self):
        return self.title


# class UserProfile(models.Model): # This might not be necceary if I'm using
# join tables. 

