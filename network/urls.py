
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("create", views.create, name="create"),
    

    #API Routes
    path("edit/<str:post_id>", views.edit, name="edit"), 
    path("follow/<int:id>", views.follow, name="follow"),
    path("like/<str:post_id>", views.like, name="like"), 
    
]
