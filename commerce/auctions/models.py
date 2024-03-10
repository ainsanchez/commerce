from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'images/', default = "")

    def __str__(self):
        return f"{self.title} {self.price}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    items = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"{self.user}: {self.items}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ManyToManyField(Listings, blank = True, related_name="sale")
    value = models.IntegerField()

    def __str__(self):
        return f"{self.user} bid {self.value}" 


