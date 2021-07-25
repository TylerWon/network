from django.test import Client, TestCase

from .models import User, Post, Like

# Create your tests here.
class NetworkTest(TestCase):
    # Setup test database with data
    def setUp(self):
        user1 = User.objects.create(username="user1", password="user1", email="user1@gmail.com")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user1.followers.add(user2)
        user2.followers.add(user1)

        post = Post.objects.create(poster=user1, content="This is my first post!")

        like = Like.objects.create(liker=user1, post=post)
    
    # Test that a User is initialized properly
    def test_user(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")

        self.assertEqual(user1.username, "user1")
        self.assertEqual(user1.password, "user1")
        self.assertEqual(user1.email, "user1@gmail.com")
        self.assertEqual(user1.followers.first(), user2)
        self.assertEqual(user2.followers.first(), user1)

    # Test that a Post is initialized properly
    def test_post(self):
        user = User.objects.get(username="user1")
        post = Post.objects.get(poster=user)

        self.assertEqual(post.poster, user)
        self.assertEqual(post.content, "This is my first post!")

    # Test that a Like is initialized properly
    def test_like(self):
        user = User.objects.get(username="user1")
        post = Post.objects.get(poster=user)
        like = Like.objects.get(liker=user)

        self.assertEquals(like.liker, user)
        self.assertEquals(like.post, post)

    def test_index(self):

