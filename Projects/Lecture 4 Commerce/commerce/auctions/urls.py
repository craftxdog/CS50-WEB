from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("selectCategory/<str:titles>", views.selectCategory, name="selectCategory"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addBid/<int:listing_id>", views.addBid, name="addBid"),
    path("createListing", views.createListing, name="createListing"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("displayWatchList", views.displayWatchList, name="displayWatchList"),
    path("addWatchList/<int:listing_id>", views.addWatchList, name="addWatchList"),
    path("removeWatchList/<int:listing_id>", views.removeWatchList, name="removeWatchList"),
    path("closeAuctions/<int:listing_id>", views.closeAuctions, name="closeAuctions"),
]
