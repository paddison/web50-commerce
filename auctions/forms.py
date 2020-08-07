from django import forms

class AuctionForm(forms.Form):
    name = forms.CharField(label="Name of Your item:", max_length=64)
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=256)
    starting_bid = forms.DecimalField(label="Starting Bid:", max_digits=7, decimal_places=2)
    category = forms.ChoiceField(label="Category", choices=[
        ("Fashion", "Fashion"),
        ("Books, Movies & Music", "Books, Movies & Music"),
        ("Electronics", "Electronics"),
        ("Collectibles & Art", "Collectibles & Art"),
        ("Home & Garden", "Home & Garden"),
        ("Sporting Goods", "Sporting Goods"),
        ("Toys & Hobbies", "Toys & Hobbies"),
        ("Business & Industrial", "Business & Industrial"),
        ("Health & Beauty", "Health & Beauty"),
        ("Others", "Others")
        ])
    picture = forms.URLField(label="Link a URL of a picture:", required=False)

class BidForm(forms.Form):
    placed_bid = forms.DecimalField(label="Bid:", max_digits=7, decimal_places=2)