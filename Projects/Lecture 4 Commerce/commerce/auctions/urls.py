from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("removeWatchList/<int:listing_id>", views.removeWatchList, name="removeWatchList"),
    path("addWatchList/<int:listing_id>", views.addWatchList, name="addWatchList"),
    path("displayWatchList", views.displayWatchList, name="displayWatchList"),
    path("comment/<int:listing_id>", views.addComment, name="addComment"),
    path("addBid/<int:listing_id>", views.addBid, name="addBid"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
]
