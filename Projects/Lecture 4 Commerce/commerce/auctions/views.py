from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Bid, Category, Listing, Comment


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategory = Category.objects.all()
    return render(request, "auctions/index.html", {
        "title": "Active Listing",
        "listings": activeListings,
        "categories": allCategory
    })

def displayCategory(request):
    activeListings = Listing.objects.filter(isActive=True)
    if activeListings:
        return render(request, "auctions/displayCategory.html", {
            "title": "Categories",
            "categories": Category.objects.all(),
            "listings": activeListings
        })
    else:
        return render(request, "auctions/displayCategory.html", {
            "title": "Categories",
            "categories": Category.objects.all(),
            "message": "No Listing"
        })
    
        
def selectCategory(request, titles):
    
    if titles == "All":
        listings = Listing.objects.filter(isActive=True)
        return render(request, "auctions/index.html", {
            "title": f"{titles}",
            "listings": listings
        })
    else:
        listings = Listing.objects.filter(category__categoryName=titles, isActive=True)
        return render(request, "auctions/index.html", {
            "title": f"{titles}",
            "listings": listings
        })

# listing = Listing.objects.get(pk=listing_id)
#     listing.watchList.add(request.user)
#     return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
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


def addBid(request, listing_id):
    newBid = request.POST["newBid"]
    listing = Listing.objects.get(pk=listing_id)
    isWatchList = request.user in listing.watchList.all()
    allComments = Comment.objects.filter(listing=listing)
    isOwner = request.user.username == listing.owner.username

    if listing.price.bid < int(newBid):
        updateBid = Bid(user=request.user, bid=int(newBid))
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


def createListing(request):
    if request.method == "GET":
        allCategory = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "title": "Creating New Listing",
            "categories": allCategory
        })
    else:
        # Getting data from Form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["image"]
        owner = request.user

        # Creating Bid Object
        newBid = Bid(bid=price, user=owner)
        # Saving the object
        newBid.save()

        # Getting Category Object
        categoryData = Category.objects.get(categoryName=category)
        # Saving Category Object
        categoryData.save()

        # Creating New Listing
        newListing = Listing(title=title, description=description,
                             image=image, price=newBid, owner=owner, category=categoryData)
        # Saving The Listing
        newListing.save()

        # Redirecting to index page
        return HttpResponseRedirect(reverse("index"))


def addComment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(pk=listing_id)
        Comment.objects.create(
            comment=comment, listing=listing, user=request.user)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


def displayWatchList(request):
    watchList = request.user.user_WatchList.all()
    return render(request, "auctions/displayWatchList.html", {
        "title": "Display WatchList",
        "listings": watchList
    })


def addWatchList(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchList.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def removeWatchList(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchList.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def closeAuctions(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.isActive = False
    listing.save()
    isOwner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html", {
        "title": f"{ listing.title }",
        "listing": listing,
        "isOwner": isOwner,
        "updated": True,
        "Message": "Successfully"
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
