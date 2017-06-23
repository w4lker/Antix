from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.username

class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    href = models.CharField(max_length=50,blank=True,null=True)
    fatherid = models.IntegerField()
    fathername = models.CharField(max_length=20,blank=True,null=True)
    pri = models.IntegerField()