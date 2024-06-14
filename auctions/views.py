from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listings, Comments, Bid


def index(request):
    active_listings = Listings.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "active_listings" : active_listings,
        "categories" : categories,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


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
        return redirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories" : categories,
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]
        current_user = request.user
        price = request.POST["price"]
        bid = Bid(bid=price, user=current_user)
        bid.save()
        category_info = Category.objects.get(category_name=category)
        new_listing = Listings(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=category_info,
            owner=current_user,
        )
        new_listing.save()
        return redirect(reverse(index))


def display_categories(request, name):
    categories = Category.objects.all()
    if name == "selection":
        return render(request, "auctions/categories.html", {
            "categories" : categories,
            "categories_msg" : "<Select a category to display its details>",
        })
    else:
        category = Category.objects.get(category_name=name)
        active_listings = Listings.objects.filter(is_active=True, category=category)
        return render(request, "auctions/categories.html", {
            "active_listings" : active_listings,
            "categories" : categories,
        })

def listing_details(request, id):
    listing = Listings.objects.get(pk=id)
    in_watchlist = request.user in listing.watchlist.all()
    comments = Comments.objects.filter(listing=listing)
    bid_comment = request.session.get("bid_comment")
    latest_bid = Bid.objects.latest("bid_time")
    bid_won_by = latest_bid.user
    if 'bid_comment' in request.session:
        del request.session["bid_comment"]
    if listing.owner == request.user:
        is_owner = True
    else:
        is_owner = False
    return render(request, "auctions/listing_details.html", {
        "listing" : listing,
        "in_watchlist" : in_watchlist,
        "comments" : comments,
        "bid_comment" : bid_comment,
        "bid_won_by" : bid_won_by,
        "is_owner" : is_owner,
    })

def place_bid(request, id):
    bid_amount = request.POST["place_bid"]
    listing = Listings.objects.get(pk=id)
    new_watchlist = listing.watchlist.add(request.user)
    if float(bid_amount) > listing.price.bid:
        bid = Bid(bid=bid_amount, user=request.user)
        bid.save()
        listing.price = bid
        listing.bid_count += 1
        listing.save()
        request.session["bid_comment"] = "Bid successful..."
        return redirect(reverse("listing_details", kwargs={"id" : id}))
    else:
        request.session["bid_comment"] = "Bid unsuccessful..."
        return redirect(reverse("listing_details", kwargs={"id" : id}))

def close_listing(request, id):
    listing = Listings.objects.get(pk=id)
    listing.is_active = False
    listing.watchlist.add(request.user)
    listing.save()
    return redirect(reverse("listing_details", kwargs={"id" : id}))
    

def watchlist(request):
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def add_watchlist(request, id):
    listing = Listings.objects.get(pk=id)
    new_watchlist = listing.watchlist.add(request.user)
    return redirect(reverse("listing_details", kwargs={"id" : id}))

def remove_watchlist(request, id):
    listing = Listings.objects.get(pk=id)
    new_watchlist = listing.watchlist.remove(request.user)
    return redirect(reverse("listing_details", kwargs={"id" : id}))

def add_comment(request, id):
    listing = Listings.objects.get(pk=id)
    comment = request.POST["comment"]
    new_comment = Comments(
        author=request.user,
        listing=listing,
        comment=comment
        )
    new_comment.save()
    return redirect(reverse("listing_details", kwargs={"id" : id}))