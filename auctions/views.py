from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Watchlist, Comment, Bid


def index(request):
    listings = Listing.objects.exclude(close_status=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea())
    starting_bid = forms.IntegerField()
    image = forms.URLField(max_length=256, required=False)
    category = forms.CharField(max_length=32, required=False)


@login_required(login_url='/')
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            listing = Listing(creator=request.user, title=title, description=description,
                              current_bid=starting_bid, image=image, category=category)
            listing.save()
            id = listing.id
            return HttpResponseRedirect(reverse("listing_page", args=(id,)))
    if request.user.is_authenticated:
        return render(request, "auctions/addListing.html", {
            "form": ListingForm()
        })


def listPage(request, list_id):
    try:
        myList = Listing.objects.get(id=list_id)
    except:
        return HttpResponse("Page not found")

    # Gets the highest bidder for the listing else False
    try:
        bidder = Bid.objects.get(listing=myList, price=myList.current_bid).bidder.username
    except:
        bidder = False

    watchlist = True

    # If the listing is watchlisted the user will see the delete from watchlist button or vice versa
    if request.user.is_authenticated:
        try:
            Watchlist.objects.get(user=request.user, item=myList)
            watchlist = True
        except:
            watchlist = False

    # Gets all the comments for the listing
    comments = myList.comments.all()
    return render(request, "auctions/listing.html", {
        "listing": myList,
        "watchlistStatus": watchlist,
        "highest_bidder": bidder,
        "comments": comments
    })


def addToWatchlist(request):
    if request.method == "POST":
        action = request.POST["action"]
        listid = request.POST["listid"]
        listing = Listing.objects.get(id=listid)
        if action == "delete":
            watchlist_item = Watchlist.objects.get(user=request.user, item=listing)
            watchlist_item.delete()
        elif action == "add":
            watchlist_item = Watchlist(user=request.user, item=listing)
            watchlist_item.save()
        return HttpResponseRedirect(reverse("listing_page", args=(listid,)))

# Handles request when bid is placed


def placeBid(request):
    if request.method == "POST":
        price = int(request.POST["price"])
        listid = request.POST["listid"]
        listing = Listing.objects.get(id=listid)

        # Server-side verification for the bidding
        if listing.creator == request.user:
            return HttpResponse("Creator cannot Bid")
        if price <= listing.current_bid:
            return HttpResponseRedirect(reverse("listing_page", args=(listid,)))

        bid = Bid(bidder=request.user, listing=listing, price=price)
        bid.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listid,)))


def add_comment(request):
    if request.method == "POST":
        comment = request.POST["comment"]
        listid = request.POST["listid"]
        listing = Listing.objects.get(id=listid)
        new_comment = Comment(listing=listing, user=request.user, comment=comment)

        new_comment.save()

        return HttpResponseRedirect(reverse("listing_page", args=(listid,)))


def user_watchlist(request):
    watchlist = User.objects.get(id=request.user.id).watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist
    })


def close_listing(request):
    if request.method == "POST":
        mylist = Listing.objects.get(id=request.POST["listid"])
        # bidder = Bid.objects.get(listing=mylist, price=mylist.current_bid).bidder
        if request.user != mylist.creator:
            return HttpResponse("Only the creator can close the listing")
        mylist.close_status = True
        mylist.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse("Invalid request")

def categories(request):
    data = Listing.objects.values('category').filter(close_status=False).distinct()
    categories = []
    for i in data:
        if i['category'] != '':
            categories += [i['category']]
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def category_page(request, category):
    category_items = Listing.objects.filter(category=category, close_status=False)
    return render(request, 'auctions/category.html', {
        "category_items": category_items,
        "category": category
    })