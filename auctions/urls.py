from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("auctions/create/", views.create_listing, name="create"),
    path("auctions/listing/id=<int:id>/", views.listing_details, name="listing_details"),
    path("auctions/bid/listing/id=<int:id>/", views.place_bid, name="place_bid"),
    path("auctions/close/id=<int:id>/", views.close_listing, name="close_listing"),
    path("categories/<str:name>/", views.display_categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/id=<int:id>/", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/id=<int:id>/", views.remove_watchlist, name="remove_watchlist"),
    path("comment/add/id=<int:id>/", views.add_comment, name="comment"),
]
