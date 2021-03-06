from django.contrib.auth.models import AbstractUser
from django.db import models

# Represents data for a User in the User table of the database
class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "followers": [follower.username for follower in self.followers.all()],
            "following": [followee.username for followee in self.following.all()]
        }

# Represents data for a Post in the Post table of the database
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "likes": self.likes.all().count(),
            "likers": [like.liker.username for like in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

# Represents data for a Like in the Like table of the database
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
