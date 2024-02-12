from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'images/', default = "")

    def __str__(self):
        return f"{self.title} {self.price}"

