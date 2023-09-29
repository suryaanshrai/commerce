from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", editable=False)

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    current_bid = models.IntegerField()
    image = models.URLField(max_length=256, blank=True)
    category = models.CharField(max_length=32, blank=True)

    close_status = models.BooleanField(default=False)

    def __str__(self):
        if self.close_status == True:
            status = "closed"
        else:
            status = "open"
        return f"{self.title} {status} at {self.current_bid}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    price = models.IntegerField()

    def __str__(self):
        return f"{self.bidder} bids {self.price} for {self.listing.title}"

    def save(self, *args, **kwargs):
        if self.price <= self.listing.current_bid:
            return False
        else:
            listing = self.listing
            listing.current_bid = self.price
            listing.save()
            super().save(*args, **kwargs)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items")