from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Post, User, Likes
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from .models import User
class postForm(forms.Form):
    thepost = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder': 'Add your post here...','style':'height: 100px; width: 100%'},))

def index(request):
    # Order all posts in timestamp order
    post_items = Post.objects.all().order_by('-date')
    
    p = Paginator(post_items, 10)
    page_num = request.GET.get('page', 1)
    # We get the page_num from url and add a default page

    #page is the page that shows up
    try:
        page = p.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = p.page(1)
  

        

    return render(request, "network/index.html",{
        "form": postForm(),
        "allposts": page
    })


#Api edit post function
@login_required
@csrf_exempt
def edit(request, post_id):
    
    # Get the post only if the user is the current user
    # Only user that made the post can edit the post
    # It also has the post id given
    post = Post.objects.get(pk=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data["des"])
        if data.get("des") is not None:
            post.des = data["des"]
        
        post.save()
        return HttpResponse(status=204)


#Api like post function
@login_required
@csrf_exempt
def like(request, post_id):

    post = Post.objects.get(pk=post_id)
    
        
    if request.method == "GET":
        
        print(Likes.objects.filter(post=post).count())
        return JsonResponse([Likes.objects.filter(post=post).count(), Likes.objects.filter(post = post, user = request.user).count()>0], safe=False)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('likes'):
            like = Likes(user = request.user, post = post)
            like.save()
            post.liked.add(request.user)
            post.likes.add(like)
            post.save()
        else:
            #unlike
            Likes.objects.filter(user = request.user, post = post).delete()
            post.liked.remove(request.user)
            post.save()

        

        return HttpResponse(status=204)
        






@login_required
def following(request):
    currentUser = request.user
    post_items = Post.objects.filter(user__in = currentUser.following.all()).order_by('-date')
    
    p = Paginator(post_items, 10)
    page_num = request.GET.get('page', 1)
    # We get the page_num from url and add a default page

    #page is the page that shows up
    try:
        page = p.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = p.page(1)
  
    return render(request, "network/following.html", {
        "allposts": page
    })


@login_required
@csrf_exempt
def follow(request, id):
    theUser = User.objects.get(pk = id)

    if request.method == "GET":
        return JsonResponse([theUser.following.all().count(), theUser.followers.all().count()], safe=False)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('follow'):
            theUser.followers.add(request.user)
            theUser.save()
            request.user.following.add(theUser)
            request.user.save()
        else:
            #unfollow
            theUser.followers.remove(request.user)
            theUser.save()
            request.user.following.remove(theUser)
            request.user.save()

        

        return HttpResponse(status=204)


def profile(request, id):
    theUser = User.objects.get(pk = id)
    post_items = Post.objects.filter(user=theUser)[::-1]
    
    p = Paginator(post_items, 10)
    page_num = request.GET.get('page', 1)
    # We get the page_num from url and add a default page

    #page is the page that shows up
    try:
        page = p.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = p.page(1)
  

    return render(request, "network/profile.html",{
        "theuser": theUser,
        "userPosts": page
    })



@login_required
def create(request):
    if request.method == "POST":
        createForm = postForm(request.POST)
        
        if createForm.is_valid():
            success = True
            user = request.user
            des = createForm.cleaned_data["thepost"]
            
            date = datetime.datetime.now()
            thePost = Post(user = user, des = des, date = date)
            thePost.save()
        else:
            success = False
             
    post_items = Post.objects.all().order_by('-date')
    
    p = Paginator(post_items, 10)
    page_num = request.GET.get('page', 1)
    # We get the page_num from url and add a default page

    #page is the page that shows up
    try:
        page = p.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = p.page(1)

    return render (request, "network/index.html", {
        "form": postForm(),
        "success": success,
        "allposts": page
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
