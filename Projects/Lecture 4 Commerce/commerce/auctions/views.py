from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategory = Category.objects.all()
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": activeListings,
        "categories": allCategory
    })

def removeWatchList(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchList.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def addWatchList(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchList.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    allComments = Comment.objects.filter(listing=listing)
    isOwner = request.user.username == listing.owner.username
    try:
        isWatchList = request.user in listing.watchList.all()
    except:
        isWatchList = False
    return render(request, "auctions/listing.html", {
        "title": f"{listing.title}",
        "listing": listing,
        "isWatchList": isWatchList,
        "allComments": allComments,
        "isOwner": isOwner
    })
    
def closeAuction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.isActive = False
    listing.save()
    isOwner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html", {
        "title": f"{listing.title}",
        "listing": listing,
        "isOwner": isOwner,
        "updated": True,
        "message": "Successfully"
    })
    
def displayWatchList(request):
    watchList = request.user.user_watchlist.all()
    return render(request, "auctions/watchList.html", {
        "title": "Watch List",
        "listings": watchList
    })

def addBid(request, listing_id):
    mewBid = request.POST["newBid"]
    listing = Listing.objects.get(id=listing_id)
    isWatchList = request.user in listing.watchList.all()
    allComments = Comment.objects.filter(listing=listing)
    isOwner = request.user.username == listing.owner.username
    if listing.price.bid < int(mewBid):
        updateBid = Bid(user=request.user, bid=int(mewBid))
        updateBid.save()
        listing.price = updateBid
        listing.save()
        return render(request, "auctions/listing.html", {
            "title": f"{listing.title}",
            "listing": listing,
            "message": "Successfully",
            "updated": True,
            "isWatchList": isWatchList,
            "allComments": allComments,
            "isOwner": isOwner
        })
    else:
        return render(request, "auctions/listing.html", {
            "title": f"{listing.title}",
            "listing": listing,
            "message": "Not Successfully",
            "updated": False,
            "isWatchList": isWatchList,
            "allComments": allComments
        })

def addComment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(id=listing_id)
        Comment.objects.create(comment=comment, listing=listing, user=request.user)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        category = Category.objects.get(categoryName=categoryFromForm)
        categoryListings = Listing.objects.filter(category=category, isActive=True)
        allCategory = Category.objects.all()
        return render(request, "auctions/index.html", {
            "title": f"{category} Listings",
            "listings": categoryListings,
            "categories": allCategory
        })

def createListing(request):
    if request.method == "GET":
        allCategory = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "title": "Create New Listing",
            "categories": allCategory
        })
    else:
        # Getting data from form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        imageURL = request.POST["image"]
        owner = request.user

        # Creating a Bid object
        newBid = Bid(bid=price, user=owner)
        newBid.save()

        # Getting category object
        categoryData = Category.objects.get(categoryName=category)
        categoryData.save()
        # Creating new listing
        newListing = Listing(title=title, description=description, imageURL=imageURL, price=newBid, owner=owner, category=categoryData)
        # Saving new listing
        newListing.save()
        # Redirecting to index page
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
