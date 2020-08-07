from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=32)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    picture = models.URLField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    closed = models.BooleanField(default=False)

    def __str__(self):
        creator = " ".join([i.capitalize() for i in str(self.created_by).split(" ")])
        return f"{self.name}, created by: {creator} on {self.created_on}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=7, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        creator = " ".join([i.capitalize() for i in str(self.user).split(" ")])
        return f"Comment on {self.auction.name} by {creator} on {self.created_on}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist")