from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListing, NewComment
from .models import User, Listings, Watchlist, Bid, Comment


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
    

# Display listings by category
def listCategories(request):
    cats = Listings.objects.all().values("category").distinct()
    return render(request, "auctions/categories.html", {
        "cats": cats
    })
    

# Display filtered listings by category
def filteredListings(request, cat_category):
    listings = Listings.objects.filter(category=cat_category)
    context = {
        'listings': listings
    }
    return render(request, "auctions/index.html", context)
    

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


# Display all items registered on the user's watchlist
@login_required
def watchlist(request):
    cart = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "cart": cart,
    })


# Display the selected listing
def display(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        form = NewComment
        thread = Comment.objects.filter(item=listing)
        #First check if listing has bids on it
        try:
            winner = Bid.objects.filter(item=listing).order_by("-value")[0] 
            user = User.objects.get(pk=request.user.id)
            user_highest_bid = Bid.objects.filter(item=listing, user=user).order_by("-value")[0]
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "winner": winner,
                "user": user,
                "user_highest_bid": user_highest_bid,
                "thread": thread,
                "form": form
            })
        except (ObjectDoesNotExist, IndexError):
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "form": form,
                "thread": thread
            })
    return render(request, "auctions/listing.html", {
    "listing": listing
    })


# Place a bid on a listing
@login_required
def bidResults(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        bid = request.POST["bid"]
        # Identify if current bid is the highest
        #highest_bid = Bid.objects.filter(item=listing, user=user).order_by("-value")[0]
        winner = Bid.objects.filter(item=listing).order_by("-value")[0]            
        try:
            if int(bid) >= winner.value or int(bid) >= listing.price:
                entry = Bid.objects.create(user=user, value=bid)
                entry.item.add(listing)
                return render(request, "auctions/listing.html")
            else:
                return HttpResponse(f"<p>Bid value has to be higher than ${winner.value}</p>")
        except ValueError:
            return HttpResponse('<p>You have to add a valid bid value</p>')


# Close listing by the user
@login_required
def closeListing(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        listing.status = 'CL'
        listing.save()
        return HttpResponseRedirect(reverse("index"))


# Create a comment for a listing
@login_required
def commentPost(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        form = request.POST["review"]
        entry = Comment(user=user, item=listing, review=form)
        entry.save()
        try:
            thread = Comment.objects.filter(item=listing)
            if len(thread) > 0:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "thread": thread
                })
        except (ObjectDoesNotExist, IndexError):
            return render(request, "auctions/listing.html", {
                "listing": listing,
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
        })      



     
        





