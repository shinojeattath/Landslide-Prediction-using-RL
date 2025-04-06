from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UnusualActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    activity_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} reported at {self.location}"
class MyUser(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username