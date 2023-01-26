from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    bid = models.FloatField(default=0.0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid}"


class Category(models.Model):
    categoryName = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.categoryName}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    price = models.ForeignKey(
        Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchList = models.ManyToManyField(
        User, blank=True, null=True, related_name="user_WatchList")

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")

    def __str__(self):
        return f"{self.user} Comment on {self.listing}"
