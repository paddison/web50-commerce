
def getCurBid(auction):
    if auction.bids.order_by("created_on").reverse().first():
        return auction.bids.order_by("created_on").reverse().first()
    else:
        return None

categorylist = [

        ("Fashion", "Fashion"),
        ("Books, Movies & Music", "Books, Movies & Music"),
        ("Electronics", "Electronics"),
        ("Collectibles & Art", "Collectibles & Art"),
        ("Home & Garden", "Home & Garden"),
        ("Sporting Goods", "Sporting Goods"),
        ("Toys & Hobbies", "Toys & Hobbies"),
        ("Business & Industrial", "Business & Industrial"),
        ("Health & Beauty", "Health & Beauty"),
        ("Others", "Select A Category")
        ]