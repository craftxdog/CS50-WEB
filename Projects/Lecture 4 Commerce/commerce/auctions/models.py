from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categoryName}"


class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid}"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    imageURL = models.CharField(max_length=100)

    # When creating the bid model, I will add a foreign key to the listing model on price field
    # price = models.FloatField()
    price = models.ForeignKey(
        Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    # This is the change I Mede to the model on price field to make it a foreign key to the bid model

    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchList = models.ManyToManyField(
        User, blank=True, null=True, related_name="user_watchlist")

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    comment = models.CharField(max_length=150)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="user_comment")

    def __str__(self):
        return f"{self.user} Comment on {self.listing}"
