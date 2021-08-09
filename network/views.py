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
            user = User.objects.create_user(username=username, email=email, password=password)
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
    
    # Return all posts
    elif request.method == "GET":
        posts = Post.objects.all().order_by("-timestamp")
        return JsonResponse([post.serialize() for post in posts], status=200, safe=False)
    
    # Do nothing 
    else:
        return JsonResponse({"message": "GET or POST request required."}, status=400)

# API route: GET = retrieves all posts created by a user
@login_required
def user_posts(request, username):
    # If request is not GET, do nothing
    if request.method != "GET":
        return JsonResponse({"message": "GET request required."}, status=400)
    
    # Get user with username=usernamee
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User does not exist."}, status=400) 
    
    # Return posts created by a user in reverse chronological order
    posts = Post.objects.filter(poster=user).order_by("-timestamp")
    return JsonResponse([post.serialize() for post in posts], status=200, safe=False)

# API route: GET = retrieve info about a user, PUT = follow or unfollow a user
def user(request, username):
    # Get user with username=username
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User does not exist."}, status=400) 

    # Return info about a user
    if request.method == "GET":
        return JsonResponse(user.serialize(), status=200, safe=False)
    
    # Update follower/following for a user
    elif request.method == "PUT":
        data = json.loads(request.body)
        follow = data.get("follow")
        username_of_user_to_follow_or_unfollow = data.get("user")

        try:
            user_to_follow_or_unfollow = User.objects.get(username=username_of_user_to_follow_or_unfollow)
        except:
            return JsonResponse({"message": "User that is trying to be followed/unfollowed does not exist."}, status=400)

        if follow:
            user.following.add(user_to_follow_or_unfollow)
            message = f"{username} is now following {username_of_user_to_follow_or_unfollow}"
        else:
            user.following.remove(user_to_follow_or_unfollow)
            message = f"{username} is no longer following {username_of_user_to_follow_or_unfollow}"
        
        user.save()

        return JsonResponse({"message": message}, status=201)

    # Do nothing
    else:
        return JsonResponse({"message": "GET request required."}, status=400)

# API route: GET = retrieves all posts made by the people a user follows
@login_required
def user_following_posts(request, username):
    # If request is not GET, do nothing
    if request.method != "GET":
        return JsonResponse({"message": "GET request required."}, status=400)
    
    # Get user with username=username
    try: 
        user = User.objects.get(username=username)
    except:
        return JsonResponse({"message": "User does not exist."}, status=400)
    
    # Return all posts made by people a user follows in reverse chronological order
    following = user.following.all()
    posts = Post.objects.filter(poster__in = following).order_by("-timestamp")
    
    return JsonResponse([post.serialize() for post in posts], status=200, safe=False)

# API route: PUT = update the content or like count for a post
@login_required
def update_post(request, post_id):
    # If request is not PUT, do nothing
    if request.method != "PUT":
        return JsonResponse({"message": "PUT request required."}, status=400)

    # Get post with id=post_id
    try:
        post = Post.objects.get(id=post_id)
    except:
        return JsonResponse({"message": "Post does not exist."}, status=400)
    
    data = json.loads(request.body)
    
    # Update content of a post
    if data.get("content") is not None:
        # If the user that made the request is not the post's poster, do nothing
        if request.user != post.poster:
            return JsonResponse({"message": "You do not have access to edit this post."}, status=404)
        
        content = data.get("content").strip()

        # If the content of the post is empty, do nothing
        if content == "":
            return JsonResponse({"message": "Post cannot be empty."}, status=400)
        
        post.content = content
        message = "Content of post successfully updated."
    
    post.save()

    return JsonResponse({"message": message}, status=201)
    
