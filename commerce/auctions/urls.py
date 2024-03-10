from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.display, name="display"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("reWatchlist/<int:items_id>", views.reWatchlist, name ="reWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name ="addWatchlist"),
    path("bidResults/<int:listing_id>", views.bidResults, name="bidResults")
]

