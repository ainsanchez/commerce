from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListing
from .models import User, Listings, Watchlist


def index(request):
    listings = Listings.objects.all()
    context = {
        'listings': listings
    }
    return render(request, "auctions/index.html", context)


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
    
def display(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing
        })

@login_required
def watchlist(request):
    cart = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "cart": cart,
    })

@login_required
def reWatchlist(request, items_id):
    if request.method == "POST":
        item = Watchlist.objects.filter(items_id=items_id)
        item.delete()
        return HttpResponseRedirect(reverse("watchlist"))
 
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
 




