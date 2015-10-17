from django.db import models
from django.utils import timezone
import datetime

class Profile(models.Model):
    text = models.CharField(max_length=4096)

    def __str__(self):
        if self.member:
            return self.member.username + ": " + self.text
        return self.text
        
# class for private messages       
class PrivateMessage(models.Model):
	text = models.CharField(max_length=4096)
	createdby = models.CharField(max_length=16)
	receives = models.CharField(max_length=16)
	mytime = models.CharField(max_length=100)
	
	def __str__(self):
		return self.text

# class for public messages	
class PublicMessage(models.Model):
	text = models.CharField(max_length=4096)
	createdby = models.CharField(max_length=16)
	receives = models.CharField(max_length=16)
	mytime = models.CharField(max_length=100)
	
	def __str__(self):
		return self.text


class Member(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    password = models.CharField(max_length=16)
    profile = models.OneToOneField(Profile, null=True)
    following = models.ManyToManyField("self", symmetrical=False)
    privateMessage = models.ManyToManyField(PrivateMessage, null = True)
    publicMessage = models.ManyToManyField(PublicMessage, null = True)
	
    def __str__(self):
        return self.username

