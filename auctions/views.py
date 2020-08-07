from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid
from .forms import AuctionForm, BidForm
from .util import getCurBid

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
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/view.html", {
                    "auction": auction,
                    "bids": bids,
                    "bidForm": BidForm(),
                    "message": "Bid must be higher than current Bid"
                })
                
    return render(request, "auctions/view.html", {
        "auction": auction, 
        "bids": bids, 
        "bidForm": BidForm(),
        })

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
        print(request.POST)
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))



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
