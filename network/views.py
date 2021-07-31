import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like

# Renders the index page
def index(request):
    return render(request, "network/index.html")

# Renders the login page
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

# Logs a user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Renders the register page
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

# API Route: POST = creates a new post, GET = retrieves all posts
def posts(request):
    # Create a new post
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)

        # Check content is non-empty, reject otherwise
        content = data.get("content").strip()
        if content == "":
            return JsonResponse({"message": "Post cannot be empty."}, status=400)

        user = request.user

        post = Post(poster=user, content=content)
        post.save()

        return JsonResponse({"message": "Post created successfully."}, status=201)
    
    # Retrieve all posts
    elif request.method == "GET":
        posts = Post.objects.all().order_by("-timestamp")
        return JsonResponse([post.serialize() for post in posts], status=200, safe=False)
    
    # Do nothing 
    else:
        return JsonResponse({"message": "GET or POST request required."}, status=400)

# API route: GET = retrieves all posts created by a user
@login_required
def user_posts(request, username):
    if request.method != "GET":
        return JsonResponse({"message": "GET request required."}, status=400)
    
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User does not exist."}, status=400) 
    
    posts = Post.objects.filter(poster=user).order_by("-timestamp")
    return JsonResponse([post.serialize() for post in posts], status=200, safe=False)

# API route: GET = retrieve info about a user
def user(request, username):
    if request.method != "GET":
        return JsonResponse({"message": "GET request required."}, status=400)
    
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User does not exist."}, status=400) 
    
    return JsonResponse(user.serialize(), status=200, safe=False)