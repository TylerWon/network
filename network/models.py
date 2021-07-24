from django.contrib.auth.models import AbstractUser
from django.db import models

# Represents data for a User in the User table of the database
class User(AbstractUser):
    pass

# Represents data for a Post in the Post table of the database
class Post(models.Model):
    pass

# Represents data for a Like in the Like table of the database
class Like(models.Model):
    pass

# Represents data for a Follower in the Follower table of the database
class Follower(models.Model):
    pass
