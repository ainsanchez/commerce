from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListing
from .models import User, Listings, Watchlist, Bid


# Display all the open listings
def index(request):
    listings = Listings.objects.all()
    context = {
        'listings': listings
    }
    return render(request, "auctions/index.html", context)


# Login the registered user
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


# Logout the registered user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a new user in the platform
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
    

# Create a new listing if form is valid
def create(request):
    if request.method == "POST":
        form = NewListing(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return HttpResponse('<p>Info Saved!</p>')
        else:
            return HttpResponse('<p>Info is not Valid!</p>')
    else:
        form = NewListing
        context = {
            'form': form
        }
        return render(request, "auctions/create.html", context)
    

# Display the selected listing
def display(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing
        })


# Display all items registered on the user's watchlist
@login_required
def watchlist(request):
    cart = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "cart": cart,
    })


# Remove item from the user's watchlist
@login_required
def reWatchlist(request, items_id):
    if request.method == "POST":
        item = Watchlist.objects.filter(items_id=items_id).filter(user_id=request.user.id)
        item.delete()
        return HttpResponseRedirect(reverse("watchlist"))
 

# Add an item to the user's watchlist if it is not already registered for that user
@login_required
def addWatchlist(request, listing_id):
    if request.method == "POST":
        item = Watchlist.objects.filter(items_id=listing_id).filter(user_id=request.user.id)
        if len(item) >= 1:
            return HttpResponse('<p>Item is already on Watchlist</p>')
        else:
            user = User.objects.get(pk=request.user.id)
            listing = Listings.objects.get(pk=listing_id)
            entry = Watchlist(user=user, items=listing)
            entry.save()
    return HttpResponseRedirect(reverse("watchlist"))

# Place a bid on a listing
@login_required
def bidResults(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = Listings.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        if bid is None:
            return HttpResponseRedirect(reverse("display"))
        else:
            entry = Bid.objects.create(user=user, value=bid)
            entry.item.add(listing)
            # Identify if current bid is the highest
            winner = Bid.objects.filter(item=listing).order_by("-value")[0]

    return render(request, "auctions/bidResults.html", {
        "entry": entry,
        "winner": winner
    })
 


""" 
            if bid == winner:
                return HttpResponse('<p>You are the winner!</p>')

 """



