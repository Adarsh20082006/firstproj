from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=150,null=True)

    def __str__(self) :
        return self.name



class Room(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50,editable=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    description=models.TextField(null=True,blank=True)
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=[ '-created','-update']

    def __str__(self):
       return self.name

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=[ '-created','-update']

    def __str__(self):
        return self.body[0:50]



    