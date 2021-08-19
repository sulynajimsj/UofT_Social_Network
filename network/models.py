from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import BooleanField, CharField, DateField, DateTimeField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.widgets import Textarea


class User(AbstractUser):
    followers = ManyToManyField("User", blank=True, related_name="theuser")
    following = ManyToManyField("User", blank=True, related_name="theUser")


class Post(models.Model):
    user = ForeignKey(User, blank=False, on_delete=CASCADE, related_name="thepost")
    des = TextField()
    date = DateTimeField()
    likes = ManyToManyField("Likes", blank=True, related_name="thePost")
    liked = ManyToManyField("User", blank=True, related_name="user")

class Likes(models.Model):
    post = ForeignKey(Post, blank=False, on_delete=CASCADE, related_name="like")
    user = ForeignKey(User, blank=False, on_delete=CASCADE, related_name="thelike")
    
