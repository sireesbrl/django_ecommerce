from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.category_name


class Listings(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    image = models.CharField(max_length = 1000)
    bid_count = models.IntegerField(default=0)
    price = models.ForeignKey("Bid", on_delete=models.CASCADE, null=False, related_name="listing_bid")
    is_active = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = "user")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = False, related_name = "category")
    watchlist = models.ManyToManyField(User, null=True, related_name="watchlist")

    def __str__(self):
        return self.title

class Bid(models.Model):
    bid = models.FloatField()
    bid_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = "user_bid")

    def __str__(self):
        return str(self.bid)

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = "author")
    listing = models.ForeignKey(Listings, on_delete = models.CASCADE, null=True, related_name="listing_comments")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
