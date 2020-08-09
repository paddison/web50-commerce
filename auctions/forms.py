from django import forms
from .util import categorylist

class AuctionForm(forms.Form):
    name = forms.CharField(label="Name of Your item:", max_length=64)
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=256)
    starting_bid = forms.DecimalField(label="Starting Bid:", max_digits=7, decimal_places=2)
    category = forms.ChoiceField(label="Category", choices=categorylist, initial="Others")
    picture = forms.URLField(label="Link a URL of a picture:", required=False)

class BidForm(forms.Form):
    placed_bid = forms.DecimalField(max_digits=7, decimal_places=2)

class WatchlistForm(forms.Form):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())
    onWatchlist = forms.BooleanField(widget=forms.HiddenInput(), required=False)

class CommentForm(forms.Form):
    comment = forms.CharField(label="Post a comment", widget=forms.Textarea(attrs={'class': 'view-comment-textarea'}), max_length=256)
    auction_id = forms.IntegerField(widget=forms.HiddenInput())