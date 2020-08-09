from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Watchlist, Comment
from .forms import AuctionForm, BidForm, WatchlistForm, CommentForm
from .util import getCurBid, categorylist

def index(request):
    auctions = Auction.objects.filter(closed=False)
    auctionData = []
    for auction in auctions:
        auctionData.append({
            "id": auction.id,
            "name": auction.name,
            "starting_bid": auction.starting_bid,
            "current_bid": getCurBid(auction).value if getCurBid(auction) else None,
            "created_by": auction.created_by,
            "created_on": auction.created_on,
            "picture": auction.picture
        }) 
    return render(request, "auctions/index.html", {"auctions": auctionData})

def add(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            auction = Auction(name=data["name"], description=data["description"], starting_bid=data["starting_bid"], category=data["category"], created_by=user, picture=data["picture"])
            auction.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionForm()
    return render(request, "auctions/add.html", {"form": form})

def view(request, id):
    
    try:
        auction = Auction.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    bids = {
        "current_bid": getCurBid(auction).value if getCurBid(auction) else None,
        "count": auction.bids.count(),
        "cur_bidder": getCurBid(auction).user if getCurBid(auction) else None,
    }

    if request.user.is_authenticated and Watchlist.objects.filter(user=request.user, auction=auction):
        onWatchlist = True
    else:
        onWatchlist = False
    data = {
        "auction": auction, 
        "bids": bids, 
        "bidForm": BidForm(),
        "watchlistForm": WatchlistForm(initial={"auction_id": auction.id, "onWatchlist": onWatchlist}),
        "onWatchlist": onWatchlist,
        "commentForm": CommentForm(initial={"auction_id": auction.id}),
        "comments": Comment.objects.filter(auction=auction).order_by("created_on").reverse()
        }

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():       
            bidValue = form.cleaned_data["placed_bid"]
            if not bids["current_bid"]:
                highestBid = auction.starting_bid
            else:
                highestBid = bids["current_bid"]
            if bidValue > highestBid:
                bid = Bid(user=request.user, auction=auction, value=bidValue)
                bid.save()
                return HttpResponseRedirect(reverse("view", kwargs={"id": auction.id}))
            else:
                data["message": "Bid must be higher than current Bid"]
                return render(request, "auctions/view.html", data)
                
    return render(request, "auctions/view.html", data)

def close(request, id):
    if request.method == "POST":
        print(request.POST)
        auction = Auction.objects.get(id=id)
        auction.closed = True
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        if form.is_valid():  
            auction = Auction.objects.get(id=form.cleaned_data["auction_id"])
            if form.cleaned_data["onWatchlist"] == True:
                watchlistlistItem = Watchlist.objects.filter(user=request.user, auction=auction)
                watchlistlistItem.delete()
            else:
                watchlistItem = Watchlist(user=request.user, auction=auction)
                watchlistItem.save()
        return HttpResponseRedirect(reverse("view", kwargs={"id": auction.id}))
    auctions = Auction.objects.filter(watchlist__user=request.user)
    return render(request, "auctions/watchlist.html", {"auctions": auctions})

def comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():  
            auction = Auction.objects.get(id=form.cleaned_data["auction_id"])
            comment = Comment(user=request.user, auction=auction, text=form.cleaned_data["comment"])
            comment.save()  
    return HttpResponseRedirect(reverse("view", kwargs={"id": auction.id}))
    
def categories(request):
    category =  [i for i,j in categorylist]
    return render(request, "auctions/categories.html", {"categories": category})

def category_view(request, category):
    auctions = Auction.objects.filter(category=category).order_by("created_on").reverse()
    return render(request, "auctions/category_view.html", {"auctions": auctions, "category": category})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")