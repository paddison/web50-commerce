from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("view/<int:id>", views.view, name="view"),
    path("close/<int:id>", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_view, name="category")
]
