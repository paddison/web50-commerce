
def getCurBid(auction):
    if auction.bids.order_by("created_on").reverse().first():
        return auction.bids.order_by("created_on").reverse().first()
    else:
        return None