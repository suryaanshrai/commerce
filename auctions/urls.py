from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/add", views.add_listing, name="add_listing"),
    path("listing/<int:list_id>", views.listPage, name="listing_page"),
    path("addToWatchlist", views.addToWatchlist, name="addToWatchlist"),
    path("placeBid", views.placeBid, name="placeBid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("watchlist", views.user_watchlist, name="user_watchlist"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_page, name="category")
]
