from django.contrib.auth.models import AbstractUser
from django.db import models

# Represents data for a User in the User table of the database
class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "followers": self.followers.count(),
            "following": self.following.count()
        }

# Represents data for a Post in the Post table of the database
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

# Represents data for a Like in the Like table of the database
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
