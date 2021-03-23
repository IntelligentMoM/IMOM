from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userinfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class User_All_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=500)
    second_name = models.CharField(max_length=500)
    contact = models.CharField(max_length=10)

class Audiofiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_name = models.CharField(max_length=500)
    audio = models.FileField(upload_to='media/')

class transcript_summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.CharField(max_length=100)
    transcript = models.TextField(max_length=5000, default="")
    summary = models.TextField(max_length=5000, default="")
